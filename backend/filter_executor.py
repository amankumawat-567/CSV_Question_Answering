import pandas as pd
import matplotlib.pyplot as plt
import io

def execute_filter_script(df: pd.DataFrame, script: str) -> pd.DataFrame:
    """
    Executes a filtering script on the provided DataFrame.

    The script should be a string representing a valid Pandas operation
    on the DataFrame `df`. It must return either:
      - a single-column DataFrame or Series if no graph is requested, or
      - a two-column DataFrame with column names matching the provided graph configuration.

    Parameters:
        df (pd.DataFrame): The original CSV DataFrame.
        script (str): The filtering script as a string.

    Returns:
        pd.DataFrame: The filtered DataFrame or Series converted to DataFrame.

    Raises:
        Exception: If the script execution fails.
    """
    try:
        result = eval(script, {"df": df, "pd": pd})
        
        if isinstance(result, pd.Series):
            result = result.to_frame()
        
        if not isinstance(result, pd.DataFrame):
            raise ValueError("The filtering script did not return a DataFrame or Series.")

        return result
    except Exception as e:
        raise Exception(f"Failed to execute filter script: {e}")

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
        if x_label not in filtered_df.columns or y_label not in filtered_df.columns:
            raise ValueError("Filtered DataFrame does not contain the required columns as specified in the graph configuration.")

        # Create a new figure for plotting
        plt.figure(figsize=(8, 6))

        if graph_type == "bar":
            plt.bar(filtered_df[x_label], filtered_df[y_label])
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title("Bar Chart")
        elif graph_type == "line":
            plt.plot(filtered_df[x_label], filtered_df[y_label], marker='o')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title("Line Chart")
        elif graph_type == "pie":
            plt.pie(filtered_df[y_label], labels=filtered_df[x_label], autopct='%1.1f%%')
            plt.title("Pie Chart")
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