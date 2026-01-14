#!/usr/bin/env python3
"""
build_all.py
A general project build helper script.
"""

import subprocess
import sys
from mypyutils import (
  find_project_root, 
  clean_directories
)

def run_generation_scripts(scripts_list):
    if not scripts_list:
        print(f"⚠️ No Python scripts set.")

    else:
        for script in scripts_list:
            print(f"\n⚙️ Running {script.name}...")
            try:
                print('SUBPROCESS FOR SCRIPT:')
                print(str(script))
                subprocess.run(
                    [sys.executable, str(script)],
                    check=True,
                )
                print(f"✅ {script.name} completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"❌ {script.name} failed with error code {e.returncode}")

def jupyterlite_build(path):
    subprocess.run(["jupyter", "lite", "build", "--output-dir", "jl-build"], cwd=path, check=True)

def run_quarto_preview(project_root):
    """
    Launch Quarto preview.
    """
    print("\n🚀 Launching Quarto preview...")
    subprocess.run(["quarto", "preview"], cwd=project_root, check=False)

def main():
    project_root = find_project_root(parent_dir="pxp2", set_path=True)

    gen_base_path = project_root / "pxp-build" / "generation"
    css_gen_path = gen_base_path / "css_generate.py"
    content_gen_path = gen_base_path / "generate.py"

    gen_scripts = [css_gen_path, content_gen_path]

    jupyterlite_base = project_root / "try-python" / "jl-notebooks"

    clean_dirs = [
        "_site",
        ".quarto",
        "try-python/jl-notebooks/jl-build"
    ]

    for c_dir in clean_dirs:
        clean_directories(base_dir=project_root, target_name=c_dir)

    run_generation_scripts(scripts_list=gen_scripts)

    jupyterlite_build(jupyterlite_base)

    run_quarto_preview(project_root)

if __name__ == "__main__":
    main()
