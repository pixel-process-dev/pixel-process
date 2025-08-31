import yaml
from pathlib import Path

from load_links import link_map
from renderers import (
  RENDERERS,
  write_section
)
from mypyutils import (
    find_project_root, 
    load_json
) 

# -----------------------
# Page Generation
# -----------------------
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

def replace_placeholders(content):
    for key, value in link_map.items():
        placeholder = "{{{" + key + "}}}"
        link = value.get('link', "")
        content = content.replace(placeholder, link)
    return content

def main():
    project_root = find_project_root(set_path=True)
    page_struct_path = project_root / "tools" / "generation" / "_json" / "links.json"
    page_data = load_json(page_struct_path)
    pxp_setup(page_data)
   
if __name__ == "__main__":
    main()