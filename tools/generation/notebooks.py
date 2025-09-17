"""
convert_for_jupyter.py

Convert a Quarto notebook into a Jupyter-friendly version:
- Raw YAML header cell → Markdown with fenced code block
- Replace or insert link placeholder ({{{link-insert}}})
- Save as <name>-jp.ipynb
"""

import nbformat as nbf
from pathlib import Path

def convert_notebook(file_path: str, link_text_qt="Use interactive notebook", link_text_jp="See original with output"):
    """
    Convert a Quarto notebook into a Jupyter-friendly version.

    Args:
        file_path (str): Path to the original .ipynb
        link_text_qt (str): Text to use in Quarto version
        link_text_jp (str): Text to use in Jupyter version
    """
    nb = nbf.read(file_path, as_version=4)
    cells = nb.cells

    # --- 1. Convert raw YAML cell to Markdown fenced block ---
    if cells and cells[0].cell_type == "raw" and cells[0].source.strip().startswith("---"):
        yaml_text = cells[0].source.strip()
        cells[0] = nbf.v4.new_markdown_cell(f"```yaml\n{yaml_text}\n```")

    # --- 2. Handle link insertion ---
    # Look for placeholder {{{link-insert}}} in any Markdown cell
    link_found = False
    for cell in cells:
        if cell.cell_type == "markdown" and "{{{link-insert}}}" in cell.source:
            # Replace with link pointing to jupyter version
            jp_name = Path(file_path).with_suffix("").name + "-jp.ipynb"
            qt_name = Path(file_path).name
            cell.source = cell.source.replace(
                "{{{link-insert}}}",
                f"[{link_text_qt}]({jp_name})"
            )
            link_found = True
            break

    # If no placeholder, append a new cross-link cell
    if not link_found:
        jp_name = Path(file_path).with_suffix("").name + "-jp.ipynb"
        link_cell = nbf.v4.new_markdown_cell(f"[{link_text_qt}]({jp_name})")
        cells.append(link_cell)

    # --- 3. Save copy as -jp.ipynb ---
    out_name = Path(file_path).with_suffix("").name + "-jp.ipynb"
    nbf.write(nb, out_name)
    print(f"✅ Converted notebook saved as {out_name}")

def convert_back(file_path: str):
    """
    Convert Jupyter-friendly version back to Quarto-ready:
    - Replace YAML fenced block with raw YAML
    - Replace link text with Quarto-friendly placeholder
    """
    nb = nbf.read(file_path, as_version=4)
    cells = nb.cells

    # --- 1. Convert first Markdown fenced block back to raw YAML ---
    if cells and cells[0].cell_type == "markdown" and cells[0].source.strip().startswith("```yaml"):
        yaml_text = cells[0].source.strip().strip("`yaml").strip("`")
        cells[0] = nbf.v4.new_raw_cell(yaml_text)

    # --- 2. Restore placeholder ---
    for cell in cells:
        if cell.cell_type == "markdown" and "Use interactive notebook" in cell.source:
            cell.source = cell.source.replace(
                cell.source,
                "{{{link-insert}}}"
            )

    out_name = str(Path(file_path).with_name(Path(file_path).stem.replace("-jp", "") + ".ipynb"))
    nbf.write(nb, out_name)
    print(f"🔄 Restored Quarto notebook saved as {out_name}")


# from convert_for_jupyter import convert_notebook, convert_back

convert_notebook("example.ipynb")
# creates example-jp.ipynb

convert_back("example-jp.ipynb")
# restores example.ipynb with placeholders
