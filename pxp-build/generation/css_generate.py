import os
from glob import glob
from mypyutils import (
    find_project_root,
    load_json,
    write_txt
)

def flatten_dict(d, prefix="", skip_list=[]):
    items = []
    for k, v in d.items():
        if k in skip_list:
            continue
        new_key = f"{prefix}-{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key))
        else:
            items.append((new_key, v))
    return items

def mix_colors(c1, c2, ratio):
    c1_list = [int(item.strip()) for item in c1.split(',')]
    c2_list = [int(item.strip()) for item in c2.split(',')]
    r = int(round(c1_list[0] * (1 - ratio) + c2_list[0] * ratio))
    g = int(round(c1_list[1] * (1 - ratio) + c2_list[1] * ratio))
    b = int(round(c1_list[2] * (1 - ratio) + c2_list[2] * ratio))
    return f"{r}, {g}, {b}"

def tokens_css(section: dict) -> str:
    token_data = section.get("tokens", {})
    lines = [":root {"]
    for key, value in flatten_dict(token_data, skip_list=["brand-colors", "base-colors", "alphas"]):
        css_var = f"--{key}".replace("_", "-")
        lines.append(f"  {css_var}: {value};")
    brand_colors = token_data.get("brand-colors", {})
    base_colors = token_data.get("base-colors", {})
    alpha_values = token_data.get("alphas", {})
    formatted_alphas = [f"{int(v*100):03d}" for v in alpha_values]
    blend_colors = {}
    for color_name, rgb in base_colors.items():
        base_var = f"--{color_name}"
        lines.append(f"  {base_var}: rgba({rgb}, 1);")
        if 'shadow' in color_name:
            blend_colors[color_name]=rgb

    for color_name, rgb in brand_colors.items():
        base_var = f"--{color_name}"
        for blend_color_name, blend_color_rgb in blend_colors.items():
            if 'light' in blend_color_name:
                mix_name = f"{base_var}-light-blend"
                mix_rgb = mix_colors(rgb, blend_color_rgb, .12)

            elif 'dark' in blend_color_name:
                mix_name = f"{base_var}-dark-blend"
                mix_rgb = mix_colors(rgb, blend_color_rgb, .16)
            lines.append(f"  {mix_name}: rgba({mix_rgb}, 1);")

        for alpha, alpha_val in zip(alpha_values,formatted_alphas):
            lines.append(f"  {base_var}-{alpha_val}: rgba({rgb}, {alpha});")

    lines.append("}")
    return "\n".join(lines)

def main_css(section: dict) -> str:
    lines = [f"{section['selector']} {{"]
    for var in section.get("variables", []):
        lines.append(f"  {var['name']}: {var['value']};")
    lines.append("}")
    return "\n".join(lines) 

def generate_css(config: dict) -> str:
    meta_type = config.get("meta", {}).get("type", "css")
    rendered_sections = []
    
    if meta_type == 'tokens':
        rendered_sections.append(tokens_css(config))
    elif meta_type == 'css':
        sections = config.get("sections", [])
        for sec in sections:
            rendered_sections.append(main_css(sec))
    else:
        print(f'Unknown type: {meta_type}.')

    return "\n\n".join(rendered_sections)

def generate_sheets(json_dir):
    json_files = glob(f'{json_dir}/*.json')
    # Ensure tokens file processed first
    json_files.sort(key=lambda f: (os.path.basename(f) != "tokens.json", f))
    for json_file in json_files:
        json_data = load_json(json_file)
        output_path = json_data.get("meta", {}).get("output_path", "output.css")
        formatted_css = generate_css(json_data)
        write_txt(output_path, formatted_css)

if __name__ == "__main__":
    project_root = find_project_root(parent_dir='pxp2', set_path=True)
    css_input_dir = project_root / "pxp-build" / "css"
    generate_sheets(json_dir=css_input_dir)
