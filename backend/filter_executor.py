import pandas as pd
import matplotlib.pyplot as plt
import io
import re  # To handle unwanted backticks

def clean_script(script: str) -> str:
    """Removes backticks and possible 'python' markers from the script."""
    return re.sub(r"^```(?:python)?\n?|```$", "", script.strip())

def execute_filter_script(df: pd.DataFrame, script: str):
    """
    Executes a filtering script on the provided DataFrame securely.

    Parameters:
        df (pd.DataFrame): The original DataFrame.
        script (str): A string containing a valid Python expression.

    Returns:
        pd.DataFrame: The filtered DataFrame or a computed result.

    Raises:
        ValueError: If the script execution fails.
    """
    script = clean_script(script)  # Clean the script
    
    print(script)

    safe_globals = {"df": df, "pd": pd}  # Allow only Pandas and the DataFrame
    try:
        result = eval(script, safe_globals)

        return result
    except Exception as e:
        raise ValueError(f"Script execution failed: {e}")

def plot_graph(filtered_df: pd.DataFrame, graph_config: dict) -> bytes:
    """
    Plots a graph based on the filtered DataFrame and graph configuration.

    The function expects the DataFrame to have exactly two columns, with
    column names matching the `x_label` and `y_label` values in the graph configuration.

    Supported graph types:
      - "bar": Bar chart
      - "line": Line chart
      - "pie": Pie chart (x_label used as labels, y_label as values)

    Parameters:
        filtered_df (pd.DataFrame): The DataFrame produced by executing the filter script.
        graph_config (dict): A dictionary with keys:
            - "type": Graph type ("bar", "line", or "pie")
            - "x_label": Name of the column for the x-axis (or labels for pie chart)
            - "y_label": Name of the column for the y-axis (or values for pie chart)
            - "is_graph_required": Boolean flag (should be True for graph plotting)

    Returns:
        bytes: The image data of the plotted graph in PNG format.

    Raises:
        Exception: If graph plotting fails or if the DataFrame does not have exactly two columns.
    """
    try:
        # Validate that the DataFrame has exactly two columns
        if filtered_df.shape[1] != 2:
            raise ValueError("For graph plotting, the filtered DataFrame must have exactly two columns.")

        x_label = graph_config.get("x_label")
        y_label = graph_config.get("y_label")
        graph_type = graph_config.get("type", "bar").lower()

        # Verify that the DataFrame contains the required columns
        x,y = list(filtered_df.columns)[:2]
        
        if x_label is None:
            x_label = x
            
        if y_label is None:
            y_label = y

        # Create a new figure for plotting
        plt.figure(figsize=(8, 6))

        if graph_type == "bar":
            plt.bar(filtered_df[x], filtered_df[y], color='blue')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title("Bar Chart")

        elif graph_type == "line":
            plt.plot(filtered_df[x], filtered_df[y], marker='o', linestyle='-', color='green')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title("Line Chart")

        elif graph_type == "scatter":
            plt.scatter(filtered_df[x], filtered_df[y], color='red')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title("Scatter Plot")

        elif graph_type == "histogram":
            plt.hist(filtered_df[y], bins=10, color='purple', edgecolor='black')
            plt.xlabel(y_label)
            plt.ylabel("Frequency")
            plt.title("Histogram")

        else:
            raise ValueError(f"Graph type '{graph_type}' is not supported.")

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        raise Exception(f"Failed to plot graph: {e}")