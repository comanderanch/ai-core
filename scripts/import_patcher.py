import sys
from pathlib import Path

def patch_ai_core_paths():
    root_path = Path(__file__).resolve().parent.parent
    if str(root_path) not in sys.path:
        sys.path.insert(0, str(root_path))



    # Add root
    if str(base_dir) not in sys.path:
        sys.path.append(str(base_dir))

    # Add ai_llm, even if it has a dash
    ai_llm_dir = base_dir / "ai_llm"
    if ai_llm_dir.exists() and str(ai_llm_dir) not in sys.path:
        sys.path.append(str(ai_llm_dir))

    # Add training, tools, memory if needed
    for folder in ["training", "tools", "scripts", "memory"]:
        subdir = base_dir / folder
        if subdir.exists() and str(subdir) not in sys.path:
            sys.path.append(str(subdir))
