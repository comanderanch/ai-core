import os
import re
from pathlib import Path
import shutil

# Step 1: Ensure ai_llm directory exists and ai_llm is a symlink
root = Path(__file__).resolve().parent.parent
ai_llm_dir = root / "ai_llm"
ai_llm_old = root / "ai_llm"

# Rename if needed
if ai_llm_old.exists() and not ai_llm_dir.exists():
    print("[•] Renaming 'ai_llm' to 'ai_llm'...")
    ai_llm_old.rename(ai_llm_dir)

# Create symlink for legacy path
if not ai_llm_old.exists():
    print("[•] Creating symbolic link 'ai_llm' → 'ai_llm'...")
    os.symlink(ai_llm_dir.name, ai_llm_old)

# Step 2: Patch Python import paths from ai_llm to ai_llm
def patch_file_imports(py_file):
    with open(py_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False
    updated_lines = []
    for line in lines:
        new_line = re.sub(r"\bai-llm\b", "ai_llm", line)
        if new_line != line:
            modified = True
        updated_lines.append(new_line)

    if modified:
        with open(py_file, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        print(f"[✓] Patched: {py_file}")

# Apply to all Python files in project
print("[•] Scanning for Python files to patch...")
for path in root.rglob("*.py"):
    if "venv" not in str(path) and "site-packages" not in str(path):
        patch_file_imports(path)

print("[✓] Patch complete.")
