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

def process_query(query: str):
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
    result = agent.run_sync(query, deps=columns)

    try:
        filtered_df = execute_filter_script(current_df, result.data.filter_script)
    except Exception as e:
        return f"Error executing filter script: {str(e)}", None

    graph_image = None
    if result.data.graph is not None and result.data.graph.is_graph_required:
        try:
            # Plot graph returns bytes; convert them to a PIL image.
            graph_image_bytes = plot_graph(filtered_df, result.data.graph.model_dump())
            graph_image = Image.open(io.BytesIO(graph_image_bytes))
        except Exception as e:
            return f"Error plotting graph: {str(e)}", None

    csv_output = filtered_df.to_csv(index=False)
    return csv_output, graph_image

# Build Gradio Interface using Blocks
with gr.Blocks() as demo:
    gr.Markdown("## CSV Query and Visualization App")
    
    with gr.Row():
        csv_input = gr.File(label="Upload CSV", file_types=[".csv"])
        upload_status = gr.Textbox(label="Upload Status", interactive=False)
    
    query_input = gr.Textbox(label="Enter your query", placeholder="Type your query here...")
    process_btn = gr.Button("Process Query")
    
    data_output = gr.Textbox(label="Filtered Data (CSV format)", lines=10)
    graph_output = gr.Image(label="Graph Output", type="pil")
    
    # Wire components together
    csv_input.change(fn=upload_csv, inputs=csv_input, outputs=upload_status)
    process_btn.click(fn=process_query, inputs=query_input, outputs=[data_output, graph_output])

if __name__ == "__main__":
    demo.launch()