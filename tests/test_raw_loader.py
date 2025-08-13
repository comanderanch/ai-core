import sys, json
from tokenizer.raw_loader import load_raw_rgb, count_colors, sha256_bytes

def main(p):
    raw = load_raw_rgb(p)
    print(json.dumps({"count": count_colors(raw),
                      "sha256": sha256_bytes(raw)}))
    sys.exit(0)

if __name__ == "__main__":
    assert len(sys.argv)==2, "usage: test_raw_loader.py <raw.bin>"
    main(sys.argv[1])
