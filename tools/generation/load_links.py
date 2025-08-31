from mypyutils import (
    find_project_root, 
    load_json
) 

project_root = find_project_root(set_path=True)
links_path = project_root / "tools" / "generation" / "_json" / "links.json"

link_map = load_json(links_path)

icons_path = project_root / "tools" / "generation" / "_json" / "icons.json"
branded_text = load_json(icons_path)
link_map.update(branded_text)

groups_path = project_root / "tools" / "generation" / "_json" / "groups.json"
groups = load_json(groups_path)

tables_path = project_root / "tools" / "generation" / "_json" / "tables.json"
tables = load_json(tables_path)