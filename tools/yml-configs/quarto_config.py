from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

def write_yaml(file_path, data):
    """Write a dict to a YAML file, preserving quotes."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        yaml.dump(data, f)

with open("_quarto_template.yml") as f:
    data = yaml.load(f)

sidebars = []
for sidebar_file in Path("sidebars").glob("*.yml"):
    with open(sidebar_file, "r") as f:
        sidebars.append(yaml.load(f))

data["website"]["sidebar"] = sidebars

f_out = Path(f"test_insert.yml")
write_yaml(f_out, data)
