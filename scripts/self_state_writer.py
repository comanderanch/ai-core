#!/usr/bin/env python3
import json, time, sys
from pathlib import Path

# optional local import for drift check (read-only)
sys.path.append("scripts")
try:
    from llm_output_resolver import LLMOutputResolver
    HAVE_RESOLVER = True
except Exception:
    HAVE_RESOLVER = False

BASE = Path(__file__).resolve().parent.parent
P_NET   = BASE / "memory" / "qbithue_network.json"
P_LEFT  = BASE / "tokenizer" / "token_set_left.json"
P_RIGHT = BASE / "tokenizer" / "token_set_right.json"
P_SNAP  = BASE / "memory" / "snapshots" / "qbithue_state_log.json"
P_OUT   = BASE / "memory" / "self" / "state.json"

def _read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def _load_qbithue_nodes(data):
    """
    Supports either:
      {"nodes": {"id": {...}}}  OR  [{"token_id": int, "hue_state": "...", "resonance": ..., "links":[...]}]
    Returns dict: id_str -> {hue_state, resonance, links}
    """
    nodes = {}
    if isinstance(data, dict) and "nodes" in data:
        for nid, nd in data["nodes"].items():
            nodes[str(nid)] = {
                "hue_state": str(nd.get("hue_state")),
                "resonance": float(nd.get("resonance", 0.0)),
                "links": list(nd.get("links", [])),
            }
    elif isinstance(data, list):
        for nd in data:
            nid = str(nd.get("token_id"))
            if nid is None: continue
            hue = nd.get("hue_state")
            # normalize possible numeric encodings
            if hue in (1, -1, 0):
                hue = {1:"WHITE", -1:"GRAY", 0:"BLACK"}[hue]
            nodes[nid] = {
                "hue_state": str(hue),
                "resonance": float(nd.get("resonance", 0.0)),
                "links": list(nd.get("links", [])),
            }
    return nodes

def _reflex_arcs(nodes, max_k=5):
    """Find GRAY -> WHITE arcs where WHITE resonance > 0."""
    arcs = []
    # compute incoming lists for convenience
    white_ids = {nid for nid, nd in nodes.items() if nd["hue_state"] == "WHITE"}
    for nid, nd in nodes.items():
        if nd["hue_state"] != "GRAY":
            continue
        for to in nd.get("links", []):
            tid = str(to)
            if tid in white_ids:
                res_w = nodes[tid].get("resonance", 0.0)
                if res_w > 0.0:
                    arcs.append({"from": str(nid), "to": tid, "res_white": round(res_w, 6)})
    # sort strongest first
    arcs.sort(key=lambda a: a["res_white"], reverse=True)
    return arcs[:max_k]

def main():
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # ensure out dir
    P_OUT.parent.mkdir(parents=True, exist_ok=True)

    net_raw   = _read_json(P_NET, [])
    left_raw  = _read_json(P_LEFT, [])
    right_raw = _read_json(P_RIGHT, [])
    snaps     = _read_json(P_SNAP, [])

    nodes = _load_qbithue_nodes(net_raw)
    blacks = sum(1 for nd in nodes.values() if nd["hue_state"] == "BLACK")
    grays  = sum(1 for nd in nodes.values() if nd["hue_state"] == "GRAY")
    whites = sum(1 for nd in nodes.values() if nd["hue_state"] == "WHITE")
    res_sum = round(sum(nd.get("resonance", 0.0) for nd in nodes.values()), 6)

    active_white = [nid for nid, nd in nodes.items() if nd["hue_state"] == "WHITE" and nd.get("resonance",0.0) > 0.0]
    arcs = _reflex_arcs(nodes, max_k=5)

    # drift check via resolver (read-only; safe)
    drift_status = "UNKNOWN"
    chosen_preview = ""
    if HAVE_RESOLVER:
        try:
            r = LLMOutputResolver().resolve_outputs()
            drift_status = "DRIFT" if r.get("drift_detected") else "OK"
            chosen_preview = (r.get("chosen_output") or "")[:160]
        except Exception:
            drift_status = "ERROR"

    last_snapshot = None
    if isinstance(snaps, list) and snaps:
        # accept last item or any item with id/timestamp
        last_snapshot = snaps[-1].get("snapshot_id") or snaps[-1].get("timestamp") or "present"

    state = {
        "timestamp": now,
        "counts": {"BLACK": blacks, "GRAY": grays, "WHITE": whites, "nodes_total": len(nodes)},
        "resonance_sum": res_sum,
        "active_white": active_white[:10],
        "top_reflex_arcs": arcs,
        "hemispheres": {"left_tokens": len(left_raw), "right_tokens": len(right_raw)},
        "drift_status": drift_status,
        "chosen_output_preview": chosen_preview,
        "last_snapshot": last_snapshot,
    }

    # write (overwrite latest self-view; additive by nature of timestamped content)
    P_OUT.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(json.dumps({"status":"OK","wrote":str(P_OUT),"active_white":len(active_white),"arcs":len(arcs),"drift":drift_status}, indent=2))

if __name__ == "__main__":
    sys.exit(main())
