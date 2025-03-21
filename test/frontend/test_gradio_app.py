#Static UI to view how UI will look

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

def static_upload_status():
    """Return a fake upload status message."""
    return "CSV uploaded successfully. Columns: col1, col2"

def static_csv_output():
    """Return a fake CSV output as a string."""
    csv_data = "col1,col2\n10,20\n30,40\n50,60"
    return csv_data

def static_graph(graph_type, x_label, y_label):
    """Generate a fake chart based on user-selected graph type."""
    plt.figure(figsize=(4,3))
    
    x_values = ['A', 'B', 'C']
    y_values = [10, 20, 30]
    
    if graph_type == "bar":
        plt.bar(x_values, y_values, color='skyblue')
    elif graph_type == "line":
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='green')
    elif graph_type == "scatter":
        plt.scatter(x_values, y_values, color='red')
    elif graph_type == "histogram":
        plt.hist(y_values, bins=3, color='purple', alpha=0.7)
    
    plt.xlabel(x_label if x_label else "X-axis")
    plt.ylabel(y_label if y_label else "Y-axis")
    plt.title(f"Fake {graph_type.capitalize()} Chart")
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return Image.open(buf)

# Build the static Gradio interface using Blocks
with gr.Blocks() as demo:
    gr.Markdown("## CSV Query and Visualization App (Static Demo)")
    
    with gr.Row():
        gr.File(label="Upload CSV (Disabled)", interactive=False)
        upload_status = gr.Textbox(value=static_upload_status(), label="Upload Status", interactive=False)
    
    query_input = gr.Textbox(value="Fake query to test frontend", label="Enter your query", interactive=True)
    
    with gr.Row():
        graph_type = gr.Dropdown(label="Graph Type", choices=["bar", "line", "scatter", "histogram"], value="bar")
        x_label = gr.Textbox(label="X-axis Label", placeholder="Enter x-axis label")
        y_label = gr.Textbox(label="Y-axis Label", placeholder="Enter y-axis label")
    
    data_output = gr.Textbox(value=static_csv_output(), label="Filtered Data (CSV format)", lines=5, interactive=False)
    graph_output = gr.Image(value=static_graph("bar", "X-axis", "Y-axis"), label="Graph Output", type="pil")
    
    def update_static_graph(graph_type, x_label, y_label):
        return static_graph(graph_type, x_label, y_label)
    
    graph_type.change(fn=update_static_graph, inputs=[graph_type, x_label, y_label], outputs=graph_output)
    x_label.change(fn=update_static_graph, inputs=[graph_type, x_label, y_label], outputs=graph_output)
    y_label.change(fn=update_static_graph, inputs=[graph_type, x_label, y_label], outputs=graph_output)
    
if __name__ == "__main__":
    demo.launch(debug=True)