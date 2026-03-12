#!/usr/bin/env python3
"""
Subconscious v1.0 — DRY RUN (read-only)
- Supports two network shapes:
  1) {"nodes": {"<id>": {"hue_state": -1|0|1 or "BLACK|GRAY|WHITE", "resonance": <num>, "links": [<id>, ...]}}}
  2) [ {"token_id": <int>, "hue_state": "BLACK|GRAY|WHITE" or -1|0|1, "resonance": <num>, "links": [<int>, ...]}, ... ]
- Prints counts and sample GRAY→WHITE arcs (resonance > 0)
- NO WRITES. Exit 0 on success; nonzero on error.
"""

import argparse, json, sys, time
from pathlib import Path
from collections import defaultdict

BLACK, GRAY, WHITE = -1, 0, +1  # FIXED: AIA V2 correct q-states
HUE_STR_TO_INT = {"BLACK": BLACK, "GRAY": GRAY, "WHITE": WHITE}
HUE_INT_TO_STR = {BLACK: "BLACK", GRAY: "GRAY", WHITE: "WHITE"}

def _load_json(p: Path):
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERR] Missing file: {p}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"[ERR] Invalid JSON in {p}: {e}", file=sys.stderr)
        return None

def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _norm_hue(v):
    # Accept "BLACK|GRAY|WHITE" or 0|-1|1
    if isinstance(v, str):
        v_up = v.strip().upper()
        if v_up in HUE_STR_TO_INT:
            return HUE_STR_TO_INT[v_up]
    if isinstance(v, (int, float)):
        iv = int(v)
        if iv in (BLACK, GRAY, WHITE):
            return iv
    return None  # unknown

def _normalize_network(net_obj):
    """
    Returns a dict: nodes = { "<id>": {"hue_state": -1|0|1, "resonance": float, "links": ["<id>", ...]} }
    Accepts either dict-form or list-form.
    """
    nodes = {}

    # Case A: dict-form with "nodes"
    if isinstance(net_obj, dict) and isinstance(net_obj.get("nodes"), dict) and net_obj.get("nodes"):
        for nid, nd in net_obj["nodes"].items():
            hue = _norm_hue(nd.get("hue_state"))
            res = float(nd.get("resonance", 0.0) or 0.0)
            raw_links = nd.get("links", []) or []
            # Keep link ids as strings for uniformity
            links = [str(l) for l in raw_links]
            nodes[str(nid)] = {"hue_state": hue, "resonance": res, "links": links}
        return nodes

    # Case B: list-form with token_id entries (your file)
    if isinstance(net_obj, list) and net_obj:
        for entry in net_obj:
            if not isinstance(entry, dict):
                continue
            tid = entry.get("token_id")
            hue = _norm_hue(entry.get("hue_state"))
            res = float(entry.get("resonance", 0.0) or 0.0)
            raw_links = entry.get("links", []) or []
            nid = str(tid) if tid is not None else None
            if nid is None or hue is None:
                # skip malformed entries quietly
                continue
            links = [str(l) for l in raw_links]
            nodes[nid] = {"hue_state": hue, "resonance": res, "links": links}
        if nodes:
            return nodes

    # Otherwise, not recognized
    return {}

def main(argv=None) -> int:
    ap = argparse.ArgumentParser("subconscious-dryrun")
    ap.add_argument("--network", default="memory/qbithue_network.json")
    ap.add_argument("--binds", default="memory/thread_binds/bind_map.json")
    ap.add_argument("--snapshots", default="memory/snapshots/qbithue_state_log.json")
    ap.add_argument("--sample", type=int, default=5, help="max samples to print")
    args = ap.parse_args(argv)

    net_p = Path(args.network)
    binds_p = Path(args.binds)
    snaps_p = Path(args.snapshots)

    net_raw = _load_json(net_p)
    if net_raw is None:
        return 2

    # binds and snapshots are optional; load if present
    binds = _load_json(binds_p) if binds_p.exists() else {}
    snaps = _load_json(snaps_p) if snaps_p.exists() else {}

    # Normalize network into {id: {...}}
    nodes = _normalize_network(net_raw)
    if not nodes:
        print(f"[ERR] {net_p} not in recognized shape or contains no usable nodes.", file=sys.stderr)
        return 3

    # Build reverse links (in-degree)
    links_in = defaultdict(int)
    for nid, nd in nodes.items():
        for tgt in nd.get("links", []) or []:
            links_in[tgt] += 1

    # Count hue states, sum resonance
    n_black = n_gray = n_white = 0
    res_sum = 0.0
    for nd in nodes.values():
        hs = nd.get("hue_state")
        if hs == BLACK: n_black += 1
        elif hs == GRAY: n_gray += 1
        elif hs == WHITE: n_white += 1
        res_sum += float(nd.get("resonance", 0.0) or 0.0)

    # Resolve GRAY→WHITE arcs with resonance(to_white) > 0
    arcs = []
    for gid, gnode in nodes.items():
        if gnode.get("hue_state") != GRAY:
            continue
        for wid in gnode.get("links", []) or []:
            wnode = nodes.get(wid)
            if not wnode:
                continue
            if wnode.get("hue_state") == WHITE and (wnode.get("resonance") or 0) > 0:
                arcs.append({"from_gray": gid, "to_white": wid, "resonance_white": float(wnode.get("resonance", 0.0))})

    # Bind lookup (best-effort; structure may vary)
    node_bind_paths = defaultdict(list)
    if isinstance(binds, dict):
        # Accept either {"paths":[...]} or {"binds":[...]} or direct list under root
        paths = []
        if isinstance(binds.get("paths"), list): paths = binds["paths"]
        elif isinstance(binds.get("binds"), list): paths = binds["binds"]
        elif isinstance(binds.get("items"), list): paths = binds["items"]
        elif isinstance(binds.get("list"), list): paths = binds["list"]
        elif isinstance(binds, list): paths = binds

        for p in paths:
            if not isinstance(p, dict): continue
            bid = p.get("id") or p.get("bind_id")
            ts  = p.get("bound_at") or p.get("timestamp")
            for nid in p.get("nodes", []) or []:
                node_bind_paths[str(nid)].append(bid if bid else "")

    # Prepare SRT samples (read-only view)
    srt_samples = []
    for idx, (nid, nd) in enumerate(nodes.items()):
        if idx >= args.sample: break
        srt_samples.append({
            "id": nid,
            "hue_state": HUE_INT_TO_STR.get(nd.get("hue_state"), str(nd.get("hue_state"))),
            "q_state": nd.get("hue_state"),
            "resonance": float(nd.get("resonance", 0.0) or 0.0),
            "links_out_count": len(nd.get("links", []) or []),
            "links_in_count": int(links_in[nid]),
            "is_emitter": bool(nd.get("hue_state") == WHITE),
            "is_reflex": bool(nd.get("hue_state") == GRAY),
            "bound_paths_count": len(node_bind_paths[nid]),
        })

    # Emit summary JSON to stdout (no file writes)
    out = {
        "timestamp": _now_iso(),
        "files": {
            "network": str(net_p),
            "binds": str(binds_p) if binds_p.exists() else None,
            "snapshots": str(snaps_p) if snaps_p.exists() else None,
        },
        "counts": {
            "BLACK": n_black, "GRAY": n_gray, "WHITE": n_white,
            "nodes_total": n_black + n_gray + n_white,
            "arcs_GRAY_to_WHITE_res>0": len(arcs),
        },
        "resonance_sum": res_sum,
        "arc_samples": arcs[:args.sample],
        "srt_samples": srt_samples,
        "invariants": {
            "no_writes": True,
            "no_llm_weight_changes": True,
            "additive_only": True
        }
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
