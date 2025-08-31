import json
import os

from scripts import (
    script_flipbook, 
    script_toggle_all,
    enable_thebe_script
)
from load_links import link_map, groups, tables

from mypyutils import (
    load_json
)

# -----------------------
# Registry setup
# -----------------------
RENDERERS = {}

def register_renderer(section_type):
    """Decorator to register a renderer for a specific section type."""
    def decorator(func):
        RENDERERS[section_type] = func
        return func
    return decorator

# -----------------------
# Renderers
# -----------------------
@register_renderer("header")
def render_header(item):
    level = item.get("level", 2)
    return f"\n{'#' * level} {item['text']}\n"

@register_renderer("text")
def render_text(item):
    return f"\n{item['markdown']}\n"

@register_renderer("header-block")
def render_header_block(item):
    img = item.get("img", "")
    name = item.get("h1", "")
    subtitle = item.get("h2", "")
    html = '\n::: {.header-block}\n\n'
    html += '![](' + img + '){.img}\n\n'
    html += f'## {name}\n'
    html += f'### {subtitle}\n'
    html += ":::\n\n"
    return html

@register_renderer("custom-callout")
def render_custom_callout(item):
    callout_type = item.get("callout-type", "")
    title = item.get("title", "")
    text = item.get("text", "")
    html = '\n::: {.callout icon="none" .custom-callout .'
    html += f'{callout_type} title="{title}"'
    html += '}\n\n' 
    html += f'{text}\n'
    html += ":::\n\n"
    return html

@register_renderer("code")
def render_code(item):
    language = item.get("language", "python")
    content = item["content"]
    html = "```{" + language + "}\n"
    html += content + '\n'
    html += "```\n"
    return html

@register_renderer("category-grid")
def render_category_grid(item):
    html = '\n<div class="category-grid">\n'

    # Case 1: Standard categories
    if "categories" in item:
        for category in item["categories"]:
            html += '<div class="category-card">\n'
            html += f"<h3>{category['title']}</h3>\n"
            if category.get("items"):
                html += "<ul>\n"
                for i in category["items"]:
                    html += f"<li>{i}</li>\n"
                html += "</ul>\n"
            html += "</div>\n"

    # Case 2: Commands
    elif "commands" in item:
        for cmd in item["commands"]:
            html += '<div class="category-card">\n'
            html += f"<h3>{cmd['name']}</h3>\n"
            html += f"<p>{cmd['description']}</p>\n"
            if cmd.get("flags"):
                html += "<ul>\n"
                for flag in cmd["flags"]:
                    html += f"<li><code>{flag['flag']}</code>: {flag['description']}</li>\n"
                html += "</ul>\n"
            html += "</div>\n"

    elif "quick-links" in item:
        for ql in item['quick-links']:
            title = ql["title"]
            page_links = ql.get("links-list", [])
            page_groups = ql.get("page-groups", [])
            for pg in page_groups:
                group_links = groups.get(pg, [])
                page_links += group_links
            html += '<div class="category-card">\n'
            html += f"<h3>{title}</h3>\n"
            html += f"<div class=\"quick-links\">"
            for page_link in page_links:
                link_data = link_map.get(page_link)
                if link_data:
                    label = link_data["label"]
                    icon = link_data["icon"]
                    href = link_data["link"]
                    desc = link_data["description"]
                    html += (
                        f'<div class="quick-link-item">'
                        f'<i class="fa-regular fa-{icon}"></i> '
                        f'<strong><a href="{href}">{label}</a></strong> → {desc}'
                        f'</div>'
                    )
            html += ("</div></div>")

    elif "text_categories" in item:
        for category in item["text_categories"]:
            html += '<div class="category-card">\n'
            html += f"<h3>{category['title']}</h3>\n"
            html += category.get("text", "")
            html += "</div>\n"

    html += "</div>\n"
    return html

@register_renderer("panel-tabset")
def render_panel_tabset(item):
    output = "\n::: {.panel-tabset}\n\n"
    tabs = item.get("tabs", [])
    for tab in tabs:
        output += f"## {tab['title']}\n"
        for section in tab.get("sections", []):
            output += write_section(section)
    output += ":::\n"
    return output

@register_renderer("collapsible")
def render_collapsible(item):
    css_class = item.get("class", "")
    html = f'<details class="{css_class}">\n'
    html += f"<summary>{item['summary']}</summary>\n"
    if item.get("content"):
        html += f"{item['content']}\n\n"
    if item.get("code"):
        language = item.get("language", "python")
        html += f"\n```{language}\n{item['code']}\n```\n"
    html += "</details>\n\n"
    return html

@register_renderer("static-tab")
def render_static_tab(item):
    css_class = item.get("class", "tab-card static-tab")
    html = f'<div class="{css_class}">\n'
    if item.get("content"):
        html += f"{item['content']}\n\n"
    if item.get("code"):
        html += f"```python\n{item['code']}\n```\n"
    html += "</div>\n\n"
    return html

@register_renderer("faqs")
def render_faqs(item):
    html = ""
    q_data = load_json(item['items_path'])
    for q in q_data:
        html += f'<h3 id=\"{q["question"]}\" class=\"visually-hidden\">{q["question"]}</h3>\n'
        html += f"""<details>\n<summary class=\"faq-summary\">{q['question']}</summary>\n\n{q['answer']}\n\n</details>\n\n"""
    return html

@register_renderer("toggle-all")
def render_toggle_all(item):
    html = f"\n<button class=\"toggle-all-button\" onclick=\"toggleAll()\">{item['text']}</button>\n\n"
    html += script_toggle_all +'\n\n'
    return html


@register_renderer("enable-thebe")
def render_enable_thebe(item):
    html = '<div id="thebe-wrapper" style="margin: 1em 0;">\n'
    html += '  <button id="enable-thebe" class="toggle-thebe-btn">🔁 Enable Interactivity</button>\n'
    html += '  <span id="thebe-status" style="margin-left: 1em; font-weight: bold; color: #555;">\n'
    html += '    Thebe: Not activated\n'
    html += '  </span>\n'
    html += '</div>\n\n'
    html += enable_thebe_script +'\n\n'
    return html


@register_renderer("page-quote")
def render_category_grid(item):
    html = '\n<div class="page-quote">\n'
    html+= f"{item['text']}\n"
    html += "</div>\n\n"
    return html

@register_renderer("divider")
def render_category_grid(item):
    html = '\n<hr class="page-divider">\n'
    return html

@register_renderer("flipbook")
def render_flipbook(item):
    image_data = load_json(item['img-json-path'])
    html = "\n```{=html}\n"
    html += "<script>\n"
    html += "const flipData = [\n"
    image_list = []
    for img in image_data['images']:
        line = '  {{ src: "{src}", caption: "{caption}" }}'.format(
            src=img["src"],
            caption=img["caption"]
        )
        image_list.append(line)
    flip_data = (',\n'.join(image_list))
    html += flip_data
    html += '\n];\n</script>\n```\n\n\n'
    html += "```{=html}\n{{< include /assets/html/flipbook.html >}}\n```\n\n"
    html += script_flipbook +'\n\n'
    return html

@register_renderer("quick-links")
def render_quick_links(item):
    """Render a list of links using icon, label, url, and description from link data."""
    page_links = item.get("page-list", [])
    page_groups = item.get("page-groups", [])
    for pg in page_groups:
        group_links = groups.get(pg, [])
        page_links += group_links

    lines = [':::{.quick-links}', '', '<ul>'] 

    for page_info in page_links:
        page_details = link_map.get(page_info)
        if page_details:
            label = page_details.get("label", "")
            url = page_details.get("link", "#")
            icon = page_details.get("icon", "window-maximize")
            icon_formatted = "{{< fa regular " + icon + " >}}" 
            description = page_details.get("description", "")
            line = f'<li class="quick-link-item">{icon_formatted} <strong><a href="{url}">{label}</a></strong> → {description}</li>'
            lines.append(line)

    lines += ['</ul>', '', ':::']  # close ul and block
    return "\n".join(lines) + "\n"

@register_renderer("markdown-table")
def render_markdown_table(item):
    table_dict = tables.get(item['table-name'], {})
    html = '\n<div class="table-cheatsheet">\n'
    html += format_markdown_table(table_dict) + "\n\n"
    html += "</div>\n\n"
    return html

def format_markdown_table(dict_rows):
    if not dict_rows:
        return ""
    headers = list(dict_rows[0].keys())
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = []
    for row in dict_rows:
        row_lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join([header_line, separator_line] + row_lines)

@register_renderer("panel-tabset-tables")
def render_panel_tables(item):
    output = "\n::: {.panel-tabset}\n\n"
    tabs = item.get("table-names", [])
    for tab in tabs:
        tab_dict = tables.get(tab, {})
        output += f"#### {tab}\n"
        output += "::: {.table-cheatsheet}\n"
        output += format_markdown_table(tab_dict) + "\n"
        output += ':::\n'
    output += ":::\n"
    return output

# -----------------------
# Recursive Rendering Logic
# -----------------------
def write_section(item, visited=None):
    """Render a section item to QMD content. Handles nested JSON paths recursively."""
    if visited is None:
        visited = set()

    # Check for json-path and merge nested content
    if "json-path" in item:
        path = item["json-path"]
        if path in visited:
            return f"\n<!-- Skipping circular reference: {path} -->\n"
        visited.add(path)
        if os.path.exists(path):
            with open(path, "r") as f:
                nested_data = json.load(f)
            # Merge nested data into current item
            item.update(nested_data)

    section_type = item.get("type")
    renderer = RENDERERS.get(section_type)
    if renderer:
        return renderer(item)
    return f"\n<!-- Unsupported type: {section_type} -->\n"