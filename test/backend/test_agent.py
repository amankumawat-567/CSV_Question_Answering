import sys
import os
# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from backend.agent import get_column_names, agent
from pydantic_ai import RunContext

def test_get_column_names():
    # Create a dummy RunContext with a list of column names.
    # Supply dummy values for model, usage, and prompt.
    context = RunContext(deps=["col1", "col2", "col3"], model="dummy", usage="dummy", prompt="dummy")
    
    try:
        # Run the asynchronous tool and print the result
        result = asyncio.run(get_column_names(context))
        print("Column names returned by get_column_names:", result)
    except Exception as e:
        print("Error in get_column_names:", e)
        
def test_agent():
    #House price dataset example
    test_columns = ['price','city','bedrooms']
    test_query = 'what is average price of a house in each city?'
    
    result = agent.run_sync(test_query, deps=test_columns)
    
    print(result.data.filter_script)
    print(result.data.graph.type)

if __name__ == "__main__":
    test_get_column_names()
    test_agent()