#!/usr/bin/env python3
import time, json, csv, argparse, itertools
from pathlib import Path

# local imports
from hemisphere_manager import HemisphereManager
from hash_token_memory import hash_token_memory_blocks
from token_size_reporter import report_token_memory_size
from llm_output_resolver import resolve_llm_output  # optional blended mode

DEFAULT_INPUT  = "training/training_set_text_tokens.csv"
DEFAULT_CYCLES = 0      # 0 = run full dataset once; >0 = limit cycle count
DEFAULT_DELAY  = 0.0
HASH_EVERY     = 3
MAX_TOKENS_BEFORE_HASH = 50

loop_log = Path("memory/snapshots/learning_loop_log.json")
loop_log.parent.mkdir(parents=True, exist_ok=True)
if not loop_log.exists():
    loop_log.write_text("[]")

def load_pairs(p: Path):
    """
    CSV schema: input_token,target_token,label,weight
    Yields target tokens as the 'spoken' token for hemisphere storage.
    """
    if not p.exists():
        print(f"[WARN] dataset not found: {p}. Falling back to synthetic cycles.")
        return None

    def gen():
        with p.open("r", encoding="utf-8", newline="") as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                try:
                    tgt = float(row["target_token"])
                except Exception:
                    continue
                yield (str(int(tgt)) if tgt.is_integer() else str(tgt))
    return gen()

def chunk(iterable, n):
    it = iter(iterable)
    while True:
        buf = list(itertools.islice(it, n))
        if not buf:
            break
        yield buf

def main():
    ap = argparse.ArgumentParser("learning-loop-runner")
    ap.add_argument("--input", default=DEFAULT_INPUT,
                    help="path to training CSV (input_token,target_token,label,weight)")
    ap.add_argument("--cycles", type=int, default=DEFAULT_CYCLES,
                    help="0 = run full dataset once; >0 = limit cycle count")
    ap.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                    help="sleep seconds between cycles")
    ap.add_argument("--batch", type=int, default=256,
                    help="tokens per cycle pushed into hemisphere")
    ap.add_argument("--blend-llm", dest="blend_llm", action="store_true",
                    help="also resolve llm_output for even cycles")
    args = ap.parse_args()

    data_path = Path(args.input)
    token_iter = load_pairs(data_path)
    using_dataset = token_iter is not None

    manager = HemisphereManager()
    hash_counter = 0
    cycle_count  = 0

    print("\n[🌀] AI-Core Learning Loop Activated")
    print("----------------------------------")
    if using_dataset:
        print(f"[i] dataset: {data_path.resolve()} (streaming)")
    else:
        print("[i] dataset: <synthetic> generated_text_cycle_X")

    def log_cycle(cycle, hemisphere, size_report, hash_status, intake_hint):
        entry = {
            "cycle": cycle,
            "intake": intake_hint,
            "hemisphere": hemisphere,
            "total_tokens": size_report['total_tokens'],
            "approx_memory_kb": size_report['approx_memory_kb'],
            "hash_status": hash_status,
            "reinforced": (cycle % 2 == 0)
        }
        logs = json.loads(loop_log.read_text())
        logs.append(entry)
        loop_log.write_text(json.dumps(logs, indent=2))

    if using_dataset:
        # each batch == one cycle
        for batch in chunk(token_iter, args.batch):
            cycle_count += 1
            hash_counter += 1
            hemisphere = "left" if cycle_count % 2 == 0 else "right"
            print(f"\n[Cycle {cycle_count}] Beginning... (batch={len(batch)})")

            manager.add_tokens(hemisphere, batch)

            try:
                left_sz  = getattr(manager, "size", lambda h: None)("left")
                right_sz = getattr(manager, "size", lambda h: None)("right")
                print(f"[dbg] hemi sizes → left:{left_sz} right:{right_sz}")
            except Exception:
                pass

            if args.blend_llm and (cycle_count % 2 == 0):
                response = resolve_llm_output(f"cycle_{cycle_count}")
                manager.add_tokens("left", response.split())

            size_report = report_token_memory_size()
            if hash_counter >= HASH_EVERY or size_report['total_tokens'] > MAX_TOKENS_BEFORE_HASH:
                block_count = hash_token_memory_blocks()
                hash_counter = 0
                hash_status = f"Hashed {block_count} blocks"
            else:
                hash_status = "No hash this cycle"

            log_cycle(cycle_count, hemisphere, size_report, hash_status,
                      intake_hint=f"tokens:{len(batch)}")
            print(f"[✓] Cycle complete. {hash_status}. Total Tokens: {size_report['total_tokens']}")

            if args.delay > 0:
                time.sleep(args.delay)

            if args.cycles > 0 and cycle_count >= args.cycles:
                break

        print("\n[🧠] Loop ended (dataset exhausted or cycle limit reached).")
    else:
        # legacy synthetic mode
        MAX_CYCLES = args.cycles if args.cycles > 0 else 100
        while cycle_count < MAX_CYCLES:
            cycle_count += 1
            hash_counter += 1
            print(f"\n[Cycle {cycle_count}] Beginning...")

            sample_input = f"generated_text_cycle_{cycle_count}"
            hemisphere = "left" if cycle_count % 2 == 0 else "right"
            if args.blend_llm and (cycle_count % 2 == 0):
                response = resolve_llm_output(sample_input)
                manager.add_tokens("left", response.split())

            size_report = report_token_memory_size()
            if hash_counter >= HASH_EVERY or size_report['total_tokens'] > MAX_TOKENS_BEFORE_HASH:
                block_count = hash_token_memory_blocks()
                hash_counter = 0
                hash_status = f"Hashed {block_count} blocks"
            else:
                hash_status = "No hash this cycle"

            log_cycle(cycle_count, hemisphere, size_report, hash_status,
                      intake_hint=sample_input)
            print(f"[✓] Cycle complete. {hash_status}. Total Tokens: {size_report['total_tokens']}")

            if args.delay > 0:
                time.sleep(args.delay)

        print("\n[🧠] Loop ended by max cycle count.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
