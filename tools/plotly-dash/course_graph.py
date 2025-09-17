import plotly.graph_objects as go
import os


def generate_course_figure(nodes, edges, title="Learning Pathway"):
    """Generate a Plotly figure object from node and edge lists."""
    id_to_index = {node["id"]: i for i, node in enumerate(nodes)}
    x_vals = [node.get("level", 0) for node in nodes]
    y_vals = list(range(len(nodes)))

    fig = go.Figure()

    for i, node in enumerate(nodes):
        fig.add_trace(go.Scatter(
            x=[x_vals[i]], y=[y_vals[i]],
            mode='markers+text',
            marker=dict(size=40, color=node.get("color", "#dddddd")),
            text=node["label"], textposition="top center",
            hoverinfo="text",
            customdata=[node.get("url", "#")]
        ))

    for source, target in edges:
        i, j = id_to_index[source], id_to_index[target]
        fig.add_shape(
            type="line",
            x0=x_vals[i], y0=y_vals[i],
            x1=x_vals[j], y1=y_vals[j],
            line=dict(color="gray", width=2)
        )

    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode='closest',
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=600
    )
    return fig


def export_course_graph(fig, output_dir, output_name, save_png=False):
    """Export figure to HTML (and optionally PNG)."""
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, f"{output_name}.html")
    fig.write_html(html_path, include_plotlyjs="cdn")
    
    if save_png:
        try:
            png_path = os.path.join(output_dir, f"{output_name}.png")
            fig.write_image(png_path)
        except Exception as e:
            print(f"[Warning] PNG export failed: {e}")
