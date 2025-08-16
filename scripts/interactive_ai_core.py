#!/usr/bin/env python3
import re
import json
import csv
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# --- Local deps on scripts/ ---
sys.path.append("scripts")
from hemisphere_manager import HemisphereManager
from token_size_reporter import report_token_memory_size
from ngram_reply_engine import load_model, generate_reply  # bigram engine

# Try to import LLM resolver; keep OFF by default while tuning
try:
    from llm_output_resolver import resolve_llm_output
    _LLM_IMPORTED = True
except Exception:
    _LLM_IMPORTED = False

# === Global feature flags (edit here) ===
HAVE_LLM = False
HAVE_NGRAM = True

# --- Paths / constants ---
BASE = Path(__file__).resolve().parent.parent
PALETTE_CSV = BASE / "tokenizer" / "full_color_tokens.csv"
MAP_JSON    = BASE / "training_data" / "word_to_token_map.json"
NGRAM_MODEL_PATH = BASE / "memory" / "ngram" / "bigram_model.json"

# New: fact anchor index (audit trail for qbithue memory)
FACT_INDEX_PATH = BASE / "memory" / "facts_index.json"

# --- Regex ---
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
_QUOTE_RE = re.compile(r'["“](.+?)["”]')
_STOP = {
    "the","a","an","and","or","but","to","of","in","on","at","for","with","by","from",
    "is","are","was","were","be","being","been","it","this","that","these","those",
    "do","does","did","can","could","should","would","may","might","will","shall",
    "i","you","we","they","he","she","my","your","our","their","his","her"
}

# --- Pending questions logger (Rule Zero safe) ---
PENDING_PATH = BASE / "training_data" / "pending_questions.txt"
def _append_pending(q: str):
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if PENDING_PATH.exists():
        existing = set(x.strip() for x in PENDING_PATH.read_text(encoding="utf-8").splitlines() if x.strip())
    q = q.strip()
    if q and q not in existing:
        with PENDING_PATH.open("a", encoding="utf-8") as f:
            f.write(q + "\n")

def _load_pending():
    if not PENDING_PATH.exists():
        return []
    return [x.strip() for x in PENDING_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]

def _write_pending(lines):
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PENDING_PATH.open("w", encoding="utf-8") as f:
        for x in lines:
            f.write(x + "\n")

def _promote_pending(index: int, answer: str):
    lines = _load_pending()
    if index < 1 or index > len(lines):
        return False, "index out of range"
    q = lines.pop(index - 1)
    _append_qa(q, answer)
    _write_pending(lines)
    return True, q

# --- Profiles (domain packs) ---
PROFILE_NAME = None  # e.g., "psychology"
# Look in BOTH places: training_data/profiles/ and top-level training_data/
PROFILE_DIRS = [BASE / "training_data" / "profiles", BASE / "training_data"]

def _available_profiles():
    names = set()
    for d in PROFILE_DIRS:
        if not d.exists():
            continue
        for p in d.glob("*_qa.txt"):
            name = p.stem  # e.g., psychology_qa
            if name.endswith("_qa"):
                name = name[:-3]
            names.add(name)
    return sorted(names)

def _profile_path(name: str):
    nm = (name or "").strip().lower()
    for d in PROFILE_DIRS:
        p = d / f"{nm}_qa.txt"
        if p.exists():
            return p
    return None

def _set_profile(name: str) -> str:
    global PROFILE_NAME
    nm = (name or "").strip().lower()
    if nm in ("off", "none", "0"):
        PROFILE_NAME = None
        _reload_qa_pairs()
        return "[i] profile: off"
    p = _profile_path(nm)
    if p:
        PROFILE_NAME = nm
        _reload_qa_pairs()
        return f"[i] profile: {nm}"
    return "[ERR] profile not found"

# --- Corpus-based Q→A retriever (fact-first) ---
BASE_CORPUS_PATHS = [
    BASE / "training_data" / "dialogue_corpus.txt",
    BASE / "training_data" / "comm_corpus.txt",
    BASE / "training_data" / "user_comm_qa.txt",
]

def _get_paths():
    paths = list(BASE_CORPUS_PATHS)
    if PROFILE_NAME:
        pp = _profile_path(PROFILE_NAME)
        if pp:
            paths.append(pp)
    return paths

def _load_qa_pairs(paths):
    pairs = []
    for path in paths:
        if not path.exists():
            continue
        cur_q = None
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("q:"):
                cur_q = line[2:].strip()
            elif line.lower().startswith("a:") and cur_q is not None:
                pairs.append((cur_q, line[2:].strip()))
                cur_q = None
    return pairs

_QA_PAIRS = _load_qa_pairs(_get_paths())

def _reload_qa_pairs():
    global _QA_PAIRS
    _QA_PAIRS = _load_qa_pairs(_get_paths())

def _append_qa(q: str, a: str):
    p = BASE / "training_data" / "user_comm_qa.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(f"Q: {q.strip()}\nA: {a.strip()}\n")
    _reload_qa_pairs()

def _norm(s: str) -> str:
    return " ".join(m.group(0).lower() for m in WORD_RE.finditer(s))

def retrieve_fact_reply(user_text: str) -> str:
    if not _QA_PAIRS:
        return ""
    u = _norm(user_text)
    for q, a in _QA_PAIRS:            # exact
        if _norm(q) == u:
            return a
    best = ""; best_len = 0            # substring fallback
    for q, a in _QA_PAIRS:
        nq = _norm(q)
        if nq in u or u in nq:
            if len(nq) > best_len:
                best, best_len = a, len(nq)
    return best

# --- Clarify-first (no guessing) ---
def _extract_topic(text: str) -> str:
    m = _QUOTE_RE.search(text)
    if m:
        topic = m.group(1).strip()
        return topic[:80] if topic else "this topic"
    toks = [t for t in WORD_RE.findall(text.lower()) if t.isalpha()]
    toks = [t for t in toks if t not in _STOP and len(t) > 2]
    topic = " ".join(toks[:3]) if toks else "this topic"
    return topic[:80]

def build_clarify_prompt(user_text: str) -> str:
    topic = _extract_topic(user_text)
    return f'clarify: "{topic}" — definition | purpose | wiring?'

# --- Recenter snapshot ---
def _recenter_log_line(state: dict) -> str:
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    keys = ["hemisphere","facts","pending","palette","vocab","llm","ngram","profile","anchors"]
    kv = ", ".join(f"{k}={state[k]}" for k in keys)
    return f"{ts} | {kv}\n"

# --- Token/Palette helpers ---
def load_palette_rows(p: Path):
    rows = []
    with p.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.reader(f); _ = next(rdr, None)
        for r in rdr:
            if not r: continue
            c = [x.strip() for x in r]
            try:
                if len(c) >= 10:
                    token = c[0]
                    R = int(float(c[6])); G = int(float(c[7])); B = int(float(c[8])); F = float(c[9])
                elif len(c) >= 6:
                    token = c[0]
                    R = int(float(c[2])); G = int(float(c[3])); B = int(float(c[4])); F = float(c[5])
                else:
                    continue
                rows.append((token, R, G, B, F))
            except Exception:
                continue
    if not rows:
        raise SystemExit(f"[ERR] no usable rows in {p}")
    return rows

def load_word_map(p: Path):
    obj = json.loads(p.read_text())
    w2i = obj.get("word_to_palette_index", {})
    return {k: int(v) for k, v in w2i.items()}

def build_inverse_maps(palette):
    freq2idx = {}
    for idx, (_tok, R, G, B, F) in enumerate(palette):
        if float(F).is_integer():
            freq2idx[str(int(F))] = idx; freq2idx[f"{int(F)}.0"] = idx
        freq2idx[str(F)] = idx
    return freq2idx

def tokenize_text(s: str):
    return [m.group(0).lower() for m in WORD_RE.finditer(s)]

def words_to_tokens(words, w2i, palette):
    out = []; M = len(palette)
    for w in words:
        idx = w2i.get(w)
        if idx is None:
            idx = (abs(hash(w)) % M)
        F = palette[idx][4]
        out.append(str(int(F)) if float(F).is_integer() else str(F))
    return out

def tokens_to_words(token_strings, inv_freq_to_idx, w2i):
    idx_to_word = {}
    for w, idx in w2i.items():
        if idx not in idx_to_word:
            idx_to_word[idx] = w
    out = []
    for t in token_strings:
        idx = inv_freq_to_idx.get(t)
        if idx is None:
            try:
                v = float(t); key = str(int(v)) if v.is_integer() else str(v)
                idx = inv_freq_to_idx.get(key)
            except Exception:
                idx = None
        out.append(idx_to_word[idx] if (idx is not None and idx in idx_to_word) else "<unk>")
    return out

# --- Fact anchor index (qbithue bridge) ---
def _load_fact_index():
    if FACT_INDEX_PATH.exists():
        try:
            return json.loads(FACT_INDEX_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"facts": []}

def _save_fact_index(obj):
    FACT_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    FACT_INDEX_PATH.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def _anchor_id(q_norm: str, a_norm: str) -> str:
    h = hashlib.sha256((q_norm + "||" + a_norm).encode("utf-8")).hexdigest()[:16]
    return f"fact:{h}"

def _ingest_pairs_into_memory(pairs, manager, w2i, palette):
    """Compile Q→A into color tokens and store in hemispheres + anchor index."""
    index = _load_fact_index()
    existing = {f["anchor"] for f in index["facts"]}
    added = 0
    for (q, a) in pairs:
        qn = _norm(q); an = _norm(a)
        anchor = _anchor_id(qn, an)
        if anchor in existing:
            continue
        q_tokens = words_to_tokens(tokenize_text(qn), w2i, palette)
        a_tokens = words_to_tokens(tokenize_text(an), w2i, palette)
        # Store deterministically: questions → RIGHT, answers → LEFT
        manager.add_tokens("right", q_tokens)
        manager.add_tokens("left", a_tokens)
        index["facts"].append({
            "anchor": anchor,
            "q": q, "a": a,
            "q_norm": qn, "a_norm": an,
            "q_tokens": q_tokens,
            "a_tokens": a_tokens,
            "hemisphere_q": "RIGHT",
            "hemisphere_a": "LEFT",
            "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        existing.add(anchor); added += 1
    _save_fact_index(index)
    return added, len(index["facts"])

def _count_anchors():
    idx = _load_fact_index()
    return len(idx.get("facts", []))

def _export_facts_txt():
    idx = _load_fact_index()
    outp = BASE / "training_data" / "exported_from_memory_qa.txt"
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8") as f:
        for item in idx.get("facts", []):
            f.write(f"Q: {item['q']}\nA: {item['a']}\n")
    return outp

def main():
    # Preflight
    if not PALETTE_CSV.exists():
        print(f"[ERR] missing palette {PALETTE_CSV}"); return 1
    if not MAP_JSON.exists():
        print(f"[ERR] missing mapping {MAP_JSON} (run text_to_color_tokens.py first)"); return 1

    palette = load_palette_rows(PALETTE_CSV)
    w2i = load_word_map(MAP_JSON)
    inv_f2i = build_inverse_maps(palette)

    # Load bigram model
    ngram_model = None
    if HAVE_NGRAM:
        if not NGRAM_MODEL_PATH.exists():
            print(f"[WARN] ngram model not found at {NGRAM_MODEL_PATH}; bigram replies disabled.")
            have_ngram_runtime = False
        else:
            try:
                ngram_model = load_model(NGRAM_MODEL_PATH); have_ngram_runtime = True
            except Exception:
                have_ngram_runtime = False
    else:
        have_ngram_runtime = False

    llm_enabled = (_LLM_IMPORTED and HAVE_LLM)

    manager = HemisphereManager()
    active = manager.get_current_hemisphere()

    print("\n[💬] AI-Core Interactive (color-token loop)")
    print("-------------------------------------------")
    print(f"[i] base path: {BASE}")
    print(f"[i] palette={len(palette)}  vocab={len(w2i)}  llm={'on' if llm_enabled else 'off'}  ngram={'on' if have_ngram_runtime else 'off'}  anchors={_count_anchors()}")
    print("[i] commands: :swap  :stats  :listqa  :teach  :teachlast  :reviewpending  :promote  :profiles  :profile <name|off>  :ingestfacts  :memfacts  :exportfacts  :recenter  :quit")
    print(f"[i] active hemisphere: {active.upper()}")

    LAST_Q = ""; LAST_A = ""

    while True:
        try:
            user = input("\nYOU> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[bye]"); break

        if not user: continue
        if user in (":quit", ":q", ":exit"):
            print("[bye]"); break

        if user == ":swap":
            manager.switch_hemisphere()
            print(f"[i] active hemisphere: {manager.get_current_hemisphere().upper()}")
            continue

        # Profiles
        if user == ":profiles":
            profs = _available_profiles()
            cur = PROFILE_NAME or "off"
            if not profs:
                print("[i] 0 profiles (put *_qa.txt in training_data/ or training_data/profiles/)")
            else:
                print(f"[i] profiles ({len(profs)}). active={cur}")
                for name in profs:
                    print(" -", name)
            continue
        if user.startswith(":profile"):
            parts = user.split(maxsplit=1)
            target = parts[1] if len(parts) > 1 else "off"
            print(_set_profile(target))
            continue

        # Teach: ":teach question | answer"
        if user.startswith(":teach "):
            try:
                payload = user[len(":teach "):]
                q, a = [x.strip() for x in payload.split("|", 1)]
                if q and a:
                    _append_qa(q, a); print("[i] taught.")
                else:
                    print("[ERR] usage: :teach question | answer")
            except Exception:
                print("[ERR] usage: :teach question | answer")
            continue

        # List known Q→A pairs
        if user == ":listqa":
            if not _QA_PAIRS:
                print("[i] 0 Q→A")
            else:
                print(f"[i] {len(_QA_PAIRS)} Q→A")
                for i, (q, a) in enumerate(_QA_PAIRS[:20], 1):
                    print(f"{i:>2}. Q: {q}\n    A: {a}")
            continue

        # Review pending unknowns
        if user == ":reviewpending":
            lines = _load_pending()
            if not lines:
                print("[i] 0 pending")
            else:
                print(f"[i] {len(lines)} pending")
                for i, q in enumerate(lines[:20], 1):
                    print(f"{i:>2}. {q}")
            continue

        # Promote a pending question: ":promote <index> | <answer>"
        if user.startswith(":promote "):
            try:
                payload = user[len(":promote "):]
                idx_str, ans = [x.strip() for x in payload.split("|", 1)]
                ok, msg = _promote_pending(int(idx_str), ans)
                print(f"[i] promoted: {msg}" if ok else f"[ERR] {msg}")
            except Exception:
                print("[ERR] usage: :promote <index> | <answer>")
            continue

        # Teach last fact answer under exact phrasing
        if user == ":teachlast":
            if LAST_Q and LAST_A:
                _append_qa(LAST_Q, LAST_A); print("[i] taught last.")
            else:
                print("[i] nothing to teach yet.")
            continue

        # Ingest Q→A into qbithue memory (color tokens + anchor index)
        if user == ":ingestfacts":
            pairs = _load_qa_pairs(_get_paths())
            added, total = _ingest_pairs_into_memory(pairs, manager, w2i, palette)
            print(f"[i] ingested {added} new fact(s) to hemispheres (anchors total={total})")
            continue

        # Count anchors stored
        if user == ":memfacts":
            print(f"[i] anchors={_count_anchors()}")
            continue

        # Export from memory index back to text (audit)
        if user == ":exportfacts":
            outp = _export_facts_txt()
            print(f"[i] exported to {outp}")
            continue

        # Recenter
        if user == ":recenter":
            state = {
                "hemisphere": manager.get_current_hemisphere().upper(),
                "facts": len(_QA_PAIRS),
                "pending": len(_load_pending()),
                "palette": len(palette),
                "vocab": len(w2i),
                "llm": "on" if llm_enabled else "off",
                "ngram": "on" if (HAVE_NGRAM and ngram_model is not None) else "off",
                "profile": PROFILE_NAME or "off",
                "anchors": _count_anchors(),
            }
            print("[i] recentered:", ", ".join(f"{k}={v}" for k, v in state.items()))
            logp = BASE / "training_data" / "recenter_log.txt"
            logp.parent.mkdir(parents=True, exist_ok=True)
            with logp.open("a", encoding="utf-8") as f:
                f.write(_recenter_log_line(state))
            continue

        if user == ":stats":
            report_token_memory_size(print_report=True); continue

        # user -> color tokens (persist to active hemisphere)
        uw = tokenize_text(user)
        u_tokens = words_to_tokens(uw, w2i, palette)
        manager.add_tokens(manager.get_current_hemisphere(), u_tokens)

        # Reply preference: FACT -> clarify -> LLM -> NGRAM -> echo
        reply_text = retrieve_fact_reply(user)

        if not reply_text:
            _append_pending(user)
            reply_text = build_clarify_prompt(user)
        else:
            LAST_Q = user; LAST_A = reply_text

        # LLM (off by default)
        if (not reply_text) and (_LLM_IMPORTED and HAVE_LLM):
            try:
                reply_text = (resolve_llm_output(user) or "").strip()
            except Exception:
                reply_text = ""

        # Bigram
        if (not reply_text) and HAVE_NGRAM and ngram_model:
            try:
                reply_text = (generate_reply(user, ngram_model, max_len=16, k=5) or "").strip()
            except Exception:
                reply_text = ""

        # Final fallback: decoded echo
        if not reply_text:
            rw = tokenize_text(user) or ["ok"]
            r_tokens = words_to_tokens(rw, w2i, palette)
            manager.add_tokens("left", r_tokens)
            decoded_words = tokens_to_words(r_tokens, inv_f2i, w2i)
            decoded_words = [w.split("_")[0] for w in decoded_words]
            print(f"AI > {' '.join(decoded_words)}")
            continue

        # Persist reply tokens
        rw = tokenize_text(reply_text)
        r_tokens = words_to_tokens(rw, w2i, palette)
        manager.add_tokens("left", r_tokens)

        print(f"AI > {reply_text}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
