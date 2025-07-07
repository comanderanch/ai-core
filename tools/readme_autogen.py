from pathlib import Path
import json

# Directories and example scripts (from prior phases)
scripts_dir = Path("scripts")
memory_dir = Path("memory")

# List all .py scripts
script_files = sorted(scripts_dir.glob("*.py"))

# Create README.md files
readmes_created = []
for script in script_files:
    readme_path = script.parent / "README.md"
    if not readme_path.exists():
        with readme_path.open("w") as f:
            f.write(f"# {script.parent.name.capitalize()} Scripts\n\n")
            f.write(f"## `{script.name}`\n")
            f.write("**Purpose**: Script auto-generated or manually developed for the AI-Core system.\n\n")
            f.write("**Description**: This script handles specific AI memory or reasoning functionality.\n")
        readmes_created.append(str(readme_path))

# Create README.md for memory/ folders if missing
memory_subdirs = [d for d in memory_dir.iterdir() if d.is_dir()]
for subdir in memory_subdirs:
    readme_path = subdir / "README.md"
    if not readme_path.exists():
        with readme_path.open("w") as f:
            f.write(f"# {subdir.name.capitalize()} Memory Logs\n\n")
            f.write("This directory contains memory data used or produced by AI-Core systems.\n")
        readmes_created.append(str(readme_path))

for path in readmes_created:
    print(f"[📘] Created README: {path}")

