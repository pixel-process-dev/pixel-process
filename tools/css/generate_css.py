import re
import os
import glob
import json
from pathlib import Path

from mypyutils import find_project_root

# ==========================
# Renderer Registry
# ==========================
RENDERERS = {}

def register_renderer(type_name):
    """Decorator to register a renderer for a given type."""
    def decorator(func):
        RENDERERS[type_name] = func
        return func
    return decorator

@register_renderer("tokens")
def render_root(section: dict) -> str:
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

@register_renderer("css")
def render_root(section: dict) -> str:
    lines = [f"{section['selector']} {{"]
    for var in section.get("variables", []):
        lines.append(f"  {var['name']}: {var['value']};")
    lines.append("}")
    return "\n".join(lines) 

@register_renderer("remove-qualifier")
def render_theme_subset(section: dict) -> str:
    selector = section["selector"]
    remove = section["remove"]
    input_css = section["initial_css_path"]
    css_dict = parse_root_css_variables(input_css)
    select_vars = {k: v for k, v in css_dict.items() if remove in k}
    renamed_vars = {
        k.replace(remove, ""): v for k, v in select_vars.items()
    }
    lines = [f"{selector} {{"]
    for k, v in renamed_vars.items():
        lines.append(f"  {k}: {v};")
    lines.append("}")
    return "\n".join(lines)

# ==========================
# Utility Functions
# ==========================
def load_json(path: str) -> dict:
    """Load a JSON file and return its content as a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_css(path: str, content: str):
    """Write CSS content to a file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def flatten_dict(d, prefix="", skip_list=[]):
    items = []
    for k, v in d.items():
        if k in skip_list:  # Skip special cases
            continue
        new_key = f"{prefix}-{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key))
        else:
            items.append((new_key, v))
    return items

def parse_root_css_variables(css_path: str) -> dict:
    """Parse CSS custom properties from the :root block into a dictionary.

    Args:
        css_path (str): Path to the CSS file.

    Returns:
        dict: Mapping of variable names to values.
    """
    with open(css_path, "r") as f:
        css = f.read()

    # Extract contents of :root { ... }
    root_match = re.search(r":root\s*{([^}]*)}", css, re.DOTALL)
    if not root_match:
        return {}

    root_block = root_match.group(1)

    # Extract lines like --var-name: value;
    var_pattern = re.compile(r"--([\w-]+)\s*:\s*([^;]+);")
    variables = {
        f"--{name.strip()}": value.strip()
        for name, value in var_pattern.findall(root_block)
    }

    return variables

def mix_colors(c1, c2, ratio):
    c1_list = [int(item.strip()) for item in c1.split(',')]
    c2_list = [int(item.strip()) for item in c2.split(',')]
    r = int(round(c1_list[0] * (1 - ratio) + c2_list[0] * ratio))
    g = int(round(c1_list[1] * (1 - ratio) + c2_list[1] * ratio))
    b = int(round(c1_list[2] * (1 - ratio) + c2_list[2] * ratio))
    return f"{r}, {g}, {b}"

# ==========================
# CSS Generation Logic
# ==========================
def generate_css(config: dict) -> str:
    """Generate CSS content from a config using registered renderers."""
    meta_type = config.get("meta", {}).get("type", "css")
    sections = config.get("sections", [])
    rendered_sections = []
    if sections:
        for sec in sections:
            renderer_name = sec.get("type", meta_type)
            renderer = RENDERERS.get(renderer_name)
            if not renderer:
                raise ValueError(f"No renderer registered for type '{renderer_name}'")
            rendered_sections.append(renderer(sec))
    else:
        renderer = RENDERERS.get(meta_type)
        if not renderer:
            raise ValueError(f"No renderer registered for type '{renderer_name}'")
        rendered_sections.append(renderer(config))
    return "\n\n".join(rendered_sections)

def generate_sheets(json_dir):
    json_files = glob.glob(f'{json_dir}/*.json')
    print(len(json_files))
    print(os.getcwd())
    print(json_dir)
    json_files.sort(key=lambda f: (os.path.basename(f) != "tokens.json", f))
    for json_file in json_files:
        json_data = load_json(json_file)
        output_path = json_data.get("meta", {}).get("output_path", "output.css")
        render_page = generate_css(json_data)
        write_css(output_path, render_page)

def css_gen_main():
    json_dir = 'tools/css/json'
    generate_sheets(json_dir=json_dir)

# ==========================
# CLI Entry Point
# ==========================
if __name__ == "__main__":
    find_project_root(marker="_quarto.yml", set_path=True)
    css_gen_main()




