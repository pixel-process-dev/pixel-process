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
from mypyutils import (
  find_project_root, 
  clean_directories,
  load_yml,
  write_yml
)
from css.generate_css import css_gen_main

def run_generation_scripts(scripts_list):
    if not scripts_list:
        print(f"⚠️ No Python scripts set.")
        return

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

def generate_quarto_yml(project_path, output_path='_quarto.yml'):
    template_path = project_path / "tools" / "yml-configs" / "quarto_template.yml"

    data = load_yml(template_path)

    sidebars = []
    sidebar_dir = template_path = project_path / "tools" / "yml-configs" / "sidebars"

    for sidebar_file in Path(sidebar_dir).glob("*.yml"):
        sidebars.append(load_yml(sidebar_file))

    data["website"]["sidebar"] = sidebars

    write_yml(output_path, data)


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
        project_root = find_project_root(parent_dir="pixel-process", set_path=True)

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
        "try-python/jl-notebooks"
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
        jupyterlite_build(build_path)

    generate_quarto_yml(project_path=project_root)

    if not args.skip_preview:
        run_quarto_preview(project_root)
    else:
        print("⏭️ Skipping Quarto preview.")

if __name__ == "__main__":
    main()
