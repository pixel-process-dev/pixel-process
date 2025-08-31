#!/usr/bin/env python3
"""
build_all.py
A general project build helper script.
"""

import os
import subprocess
from pathlib import Path
import argparse
import sys
import shutil
from mypyutils import find_project_root, clean_directories
from css.generate_css import css_gen_main

def run_generation_scripts(scripts_list):
    # script_files = sorted(scripts_dir.glob(ext))

    if not scripts_list:
        print(f"⚠️ No Python scripts set.")
        return

    for script in scripts_list:
        print(f"\n⚙️ Running {script.name}...")
        try:
            subprocess.run(
                [sys.executable, str(script)],
                check=True,
            )
            print(f"✅ {script.name} completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ {script.name} failed with error code {e.returncode}")

def jupyterlite_build(path, project_path):
    static_path = path / "custom_css" / "static"
    # Check if the directory exists
    if not static_path.exists():
        static_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory '{static_path}' created successfully.")
    css_copies = ['tokens.css', 'themes.css', 'jupyter-lite-custom.css']
    for css_file in css_copies:
        source_css = project_path / "assets" / "css" / css_file
        destination_css = static_path / css_file
        shutil.copyfile(source_css, destination_css)

    subprocess.run(["jupyter", "lite", "build", "--output-dir", "jl-build"], cwd=path,check=True)

def run_quarto_preview(project_root):
    """
    Launch Quarto preview.
    """
    print("\n🚀 Launching Quarto preview...")
    subprocess.run(["quarto", "preview"], cwd=project_root, check=False)

def main():
    parser = argparse.ArgumentParser(description="General Quarto project builder.")
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Project root path (default: auto-discovered or current directory)",
    )
    parser.add_argument(
        "--skip-preview",
        action="store_true",
        help="Skip running 'quarto preview'",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Only clean directories, do not run scripts or preview",
    )

    args = parser.parse_args()

    # Determine project root
    if args.path:
        project_root = Path(args.path).resolve()
    else:
        project_root = find_project_root()

    print(f"📂 Using project root: {project_root}")

    # Directories to clean (easily extendable)
    clean_dirs = [
        "_site",
        ".quarto",
        "_includes/generated",
    ]

    for c_dir in clean_dirs:
        clean_directories(base_dir=project_root, target_name=c_dir)

    jupyterlite_paths = [
        "jump-in/jl-notebooks"
    ]

    for jl_dir in jupyterlite_paths:
        build_dir = os.path.join(jl_dir, "jl-build")
        clean_directories(base_dir=project_root, target_name=build_dir)

    if args.clean_only:
        print("🧹 Clean-only mode complete.")
        return

    # Run generation scripts
    gen_path = project_root / "tools" / "generation" / "generate.py"

    run_generation_scripts(scripts_list=[gen_path])

    css_gen_main()

    for path in jupyterlite_paths:
        build_path = project_root / Path(path)
        jupyterlite_build(build_path, project_path=project_root)

    if not args.skip_preview:
        run_quarto_preview(project_root)
    else:
        print("⏭️ Skipping Quarto preview.")

if __name__ == "__main__":
    main()
