import yaml
from pathlib import Path
import nbformat as nbf

from load_links import link_map
from renderers import (
  RENDERERS,
  write_section
)
from mypyutils import (
    find_project_root, 
    load_json
) 


def generate_qmd_from_json(json_data, output_path):
    meta = json_data.get("meta", {})
    body = json_data.get("body", [])

    yaml_header = yaml.dump(meta, sort_keys=False)
    # Wrap in front matter
    qmd_header = f"---\n{yaml_header}---\n"

    # Body content
    content = "".join(write_section(item) for item in body)
    content = replace_placeholders(content)

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(qmd_header + content)

    print(f"Saved: {output_path}")
    return output_path

def jl_notebook_conversion(page_details):
    base_path = page_details['base_ntbk']
    output_path = page_details['save_path']
    
    in_path = Path(base_path.strip("/"))
    out_path = Path(output_path.strip("/"))
    out_parent = out_path.parent

    nb = nbf.read(in_path, as_version=4)
    cells = nb.cells

    if cells and cells[0].source.strip().startswith("---"):
        yaml_text = cells[0].source.strip()
        try:
            frontmatter = yaml.safe_load(yaml_text.strip("--- \n"))
        except Exception as e:
            print(f"⚠️ Could not parse YAML from {in_path}: {e}")
            frontmatter = {}

        md_intro = []
        if "title" in frontmatter:
            md_intro.append(f"# {frontmatter['title']}")
        if "subtitle" in frontmatter:
            md_intro.append(f"## {frontmatter['subtitle']}")
        if "description" in frontmatter:
            md_intro.append(frontmatter["description"])

        intro_cell = nbf.v4.new_markdown_cell("\n".join(md_intro).strip())
        cells[0] = intro_cell

    Path(out_parent).mkdir(parents=True, exist_ok=True)
    nbf.write(nb, out_path)
    print(f"✅ Converted notebook saved as {out_path}")

def pxp_setup(page_data):
    for page_details in page_data.values():
        build = page_details.get('generate')
        if build:
            page_path = page_details.get('link', "")
            path = Path(page_path.strip("/"))
            stem = path.stem
            parent = path.parent
            json_path = str(parent / "_json" / f"{stem}.json")
            json_data = load_json(json_path)
            if json_data:
                generate_qmd_from_json(json_data, path)
        ntbk_convert = page_details.get('base_ntbk')
        if ntbk_convert:
            jl_notebook_conversion(page_details)

def replace_placeholders(content):
    for key, value in link_map.items():
        placeholder = "{{{" + key + "}}}"
        link = value.get('link', "")
        content = content.replace(placeholder, link)
    return content

def main():
    print('Running generate script!!')
    project_root = find_project_root(parent_dir="pxp2",set_path=True)
    page_struct_path = project_root / "pxp-build" / "generation" / "_json" / "links.json"
    page_data = load_json(page_struct_path)
    pxp_setup(page_data)
   
if __name__ == "__main__":
    main()