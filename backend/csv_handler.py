import pandas as pd

def load_csv(file_obj):
    """
    Load a CSV file from a file-like object and return a Pandas DataFrame.
    
    Parameters:
        file_obj: A file-like object (e.g., as provided by Gradio's file upload component).
    
    Returns:
        pd.DataFrame: A DataFrame containing the CSV data.
    
    Raises:
        ValueError: If the CSV file cannot be loaded or is empty.
    """
    try:
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
            
        df = pd.read_csv(file_obj)
        
        if df.empty:
            raise ValueError("CSV file is empty.")
        
        return df
    except Exception as e:
        raise ValueError(f"Failed to load CSV file: {e}")


def validate_csv(file_obj):
    """
    Validate the CSV file by attempting to load it.
    Additional checks (e.g., file size, required columns) can be implemented here.
    
    Parameters:
        file_obj: A file-like object.
    
    Returns:
        bool: True if the CSV file is valid.
    
    Raises:
        ValueError: If the CSV file is invalid.
    """
    try:
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
            
        df = pd.read_csv(file_obj)
        
        if df.empty:
            raise ValueError("CSV file is empty.")
        
        return True
    except Exception as e:
        raise ValueError(f"CSV validation failed: {e}")