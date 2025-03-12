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

def static_graph():
    """Generate a fake bar chart and return it as a PIL image."""
    # Create a simple bar chart
    plt.figure(figsize=(4,3))
    plt.bar(['A', 'B', 'C'], [10, 20, 30], color='skyblue')
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Fake Bar Chart")
    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()  # Close the figure to free up memory
    buf.seek(0)
    # Open the image with PIL and return it
    return Image.open(buf)

# Build the static Gradio interface using Blocks
with gr.Blocks() as demo:
    gr.Markdown("## CSV Query and Visualization App (Static Demo)")
    
    with gr.Row():
        # Simulated, disabled CSV uploader (for display purposes)
        gr.File(label="Upload CSV (Disabled)", interactive=False)
        upload_status = gr.Textbox(value=static_upload_status(), label="Upload Status", interactive=False)
    
    # Pre-filled query input (editable if needed)
    query_input = gr.Textbox(value="Fake query to test frontend", label="Enter your query", interactive=True)
    
    # Display static CSV output
    data_output = gr.Textbox(value=static_csv_output(), label="Filtered Data (CSV format)", lines=5, interactive=False)
    
    # Display the pre-generated graph image (as a PIL image)
    graph_output = gr.Image(value=static_graph(), label="Graph Output", type="pil")
    
    # Arrange the layout
    with gr.Row():
        gr.Column([query_input])
        gr.Column([data_output, graph_output])
    
# Launch the UI
if __name__ == "__main__":
    demo.launch(debug=True)
