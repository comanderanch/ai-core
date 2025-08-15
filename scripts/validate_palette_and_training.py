#!/usr/bin/env python3
import csv, sys, argparse
from pathlib import Path

def load_raw_palette(raw_path: Path):
    rgbf_set, freq_set = set(), set()
    with raw_path.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.reader(f)
        _ = next(rdr, None)  # header
        for row in rdr:
            if not row: continue
            cols = [c.strip() for c in row]
            if len(cols) >= 10:
                # [0]=token_bin,[1]=hue_bin,[2]=red_bin,[3]=green_bin,[4]=freq_float,
                # [5]=hue_deg,[6]=R_dec,[7]=G_dec,[8]=B_dec,[9]=freq_dec
                try:
                    r = int(float(cols[6])); g = int(float(cols[7])); b = int(float(cols[8]))
                    fr = float(cols[9])
                except Exception:
                    continue
            elif len(cols) >= 6:
                # Fallback: RGB at 2..4, F at 5
                try:
                    r = int(float(cols[2])); g = int(float(cols[3])); b = int(float(cols[4]))
                    fr = float(cols[5])
                except Exception:
                    continue
            else:
                continue
            rgbf_set.add((r,g,b,fr))
            freq_set.add(fr)
    return rgbf_set, freq_set

def validate_training(train_path: Path, rgbf_set, freq_set):
    req = {"input_token","target_token","label","weight"}
    n = bad_schema = bad_numeric = not_in_palette = 0
    with train_path.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.DictReader(f)
        if not req.issubset(rdr.fieldnames or set()):
            missing = req - set(rdr.fieldnames or [])
            return {"status":"FAIL","reason":f"missing columns: {missing}"}
        for row in rdr:
            n += 1
            try:
                float(row["input_token"]); float(row["target_token"]); float(row["weight"])
            except Exception:
                bad_numeric += 1; continue
            lab = row["label"].strip().strip('"')
            parts = lab.split(",")
            if len(parts) != 4:
                bad_schema += 1; continue
            try:
                r = int(float(parts[0])); g = int(float(parts[1])); b = int(float(parts[2])); fr = float(parts[3])
            except Exception:
                bad_numeric += 1; continue
            if (r,g,b,fr) not in rgbf_set:
                not_in_palette += 1
    status = "PASS" if (bad_schema==0 and bad_numeric==0 and not_in_palette==0) else "FAIL"
    return {
        "status": status,
        "rows_checked": n,
        "issues": {
            "bad_schema": bad_schema,
            "bad_numeric": bad_numeric,
            "label_not_in_palette": not_in_palette
        }
    }

def main():
    ap = argparse.ArgumentParser("validate-palette-and-training")
    ap.add_argument("--train", default="training/training_set.csv")
    ap.add_argument("--palette", default="tokenizer/full_color_tokens.csv")
    args = ap.parse_args()

    TRAIN = Path(args.train)
    RAW   = Path(args.palette)
    if not RAW.exists(): print(f"[ERR] missing {RAW}"); return 2
    if not TRAIN.exists(): print(f"[ERR] missing {TRAIN}"); return 2

    rgbf_set, freq_set = load_raw_palette(RAW)
    if not rgbf_set:
        print("[ERR] palette parsed 0 tuples — check CSV format."); return 3

    report = validate_training(TRAIN, rgbf_set, freq_set)
    print(report)
    return 0 if report["status"]=="PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
