import sys
import os
# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
from backend.filter_executor import execute_filter_script, plot_graph

def test_execute_filter_script():
    # Create a sample DataFrame
    data = {
        "price": [100, 200, 300, 400, 500],
        "bedrooms": [1, 2, 2, 3, 4],
        "bathrooms": [1, 1, 2, 2, 3]
    }
    df = pd.DataFrame(data)
    
    # Filtering script: get rows with price greater than 200
    script = "df[(df['price'] > 200)]"
    
    try:
        filtered_df = execute_filter_script(df, script)
        print("Filtered DataFrame:")
        print(filtered_df)
    except Exception as e:
        print("Error in execute_filter_script:", e)

def test_plot_graph():
    # Create a sample DataFrame for graph plotting
    data = {
        "city": ["A", "B", "C"],
        "average_price": [300, 400, 500]
    }
    df = pd.DataFrame(data)
    
    # Graph configuration for a bar chart
    graph_config = {
        "type": "bar",
        "x_label": "city",
        "y_label": "average_price",
        "is_graph_required": True
    }
    
    try:
        image_bytes = plot_graph(df, graph_config)
        # Save the image to a file so you can inspect it
        with open("test_plot.png", "wb") as f:
            f.write(image_bytes)
        print("Graph plotted successfully and saved as 'test_plot.png'.")
    except Exception as e:
        print("Error in plot_graph:", e)

if __name__ == "__main__":
    print("Testing execute_filter_script:")
    test_execute_filter_script()
    print("\nTesting plot_graph:")
    test_plot_graph()
