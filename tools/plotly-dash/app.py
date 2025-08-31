import json
import dash
from dash import dcc, html, Input, Output
from course_graph import generate_course_figure, export_course_graph

# Load config
with open("course-paths.json") as f:
    graph_data = json.load(f)

meta = graph_data.get("meta", {})
title = meta.get("title", "Learning Pathway")
output_name = meta.get("output_name", "course-path")
output_dir = meta.get("output_dir", "site")

# Create figure
fig = generate_course_figure(graph_data["nodes"], graph_data["edges"], title=title)

# Optional: export static HTML and PNG
export_course_graph(fig, output_dir, output_name, save_png=True)

# Dash app
app = dash.Dash(__name__)
app.title = title

app.layout = html.Div([
    html.H1(title),
    dcc.Graph(id='course-graph', figure=fig),
    html.Div(id='click-output')
])


@app.callback(
    Output('click-output', 'children'),
    Input('course-graph', 'clickData')
)
def display_click(clickData):
    if clickData and clickData["points"]:
        url = clickData["points"][0]["customdata"]
        return html.A("Go to topic", href=url, target="_blank")
    return "Click a node to visit content"


if __name__ == "__main__":
    app.run(debug=True)
