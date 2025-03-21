import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image

from backend.csv_handler import load_csv 
from backend.agent import agent           
from backend.filter_executor import execute_filter_script, plot_graph

# Global variable to store the current CSV DataFrame
current_df = None

def upload_csv(file_obj):
    """
    Loads an uploaded CSV file into a global DataFrame.
    """
    global current_df
    try:
        current_df = load_csv(file_obj)
        columns = list(current_df.columns)
        return f"CSV uploaded successfully. Columns: {', '.join(columns)}"
    except Exception as e:
        return f"Error uploading CSV: {str(e)}"

def process_query(query: str, graph_type: str, x_label: str|None, y_label: str|None):
    """
    Processes the user query by:
      - Passing the query along with column names to the agent.
      - Executing the filtering script on the DataFrame.
      - Plotting a graph if required.
    
    Returns:
      - Filtered CSV output as text.
      - A PIL image for the graph (if graph is required) or None.
    """
    global current_df
    if current_df is None:
        return "No CSV uploaded", None

    # Get column names as a list and pass to the agent
    columns = list(current_df.columns)
    filter_script = agent.run_sync(query, deps=columns).data

    try:
        filtered_df = execute_filter_script(current_df, filter_script)
    except Exception as e:
        return f"Error executing filter script: {str(e)},\n #> {filter_script}", None

    graph_image = None
    if graph_type:
        try:
            graph_params = {"type": graph_type, "x_label": x_label, "y_label": y_label}
            graph_image_bytes = plot_graph(filtered_df, graph_params)
            graph_image = Image.open(io.BytesIO(graph_image_bytes))
        except Exception as e:
            return f"Error plotting graph: {str(e)}", None

    csv_output = None
    if isinstance(filtered_df, (int, float, str)):
        csv_output = filtered_df
    elif isinstance(filtered_df, pd.Series):
        csv_output = f"{filtered_df.index[0]} is {filtered_df.to_string(index=False)}"
    elif isinstance(filtered_df, pd.DataFrame):
        csv_output = filtered_df.to_csv(index=False)
        
    return csv_output, graph_image

# Build Gradio Interface using Blocks
with gr.Blocks() as demo:
    gr.Markdown("## CSV Query and Visualization App")
    
    with gr.Row():
        csv_input = gr.File(label="Upload CSV", file_types=[".csv"])
        upload_status = gr.Textbox(label="Upload Status", interactive=False)
    
    query_input = gr.Textbox(label="Enter your query", placeholder="Type your query here...")
    
    with gr.Row():
        graph_type = gr.Dropdown(label="Graph Type", choices=["", "bar", "line", "scatter", "histogram"], value="")
        x_label = gr.Textbox(label="X-axis Label", placeholder="Enter x-axis label", value=None)
        y_label = gr.Textbox(label="Y-axis Label", placeholder="Enter y-axis label", value=None)
    
    process_btn = gr.Button("Process Query")
    
    data_output = gr.Textbox(label="Filtered Data (CSV format)", lines=10)
    graph_output = gr.Image(label="Graph Output", type="pil")
    
    # Wire components together
    csv_input.change(fn=upload_csv, inputs=csv_input, outputs=upload_status)
    process_btn.click(fn=process_query, inputs=[query_input, graph_type, x_label, y_label], outputs=[data_output, graph_output])

if __name__ == "__main__":
    demo.launch()