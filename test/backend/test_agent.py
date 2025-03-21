import sys
import os
# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.agent import agent
from pydantic_ai import RunContext
        
def test_agent():
    #House price dataset example
    test_columns = ['car','price','size']
    test_query = 'what is average size of a car?'
    
    result = agent.run_sync(test_query, deps=test_columns)
    
    print(result.data)

if __name__ == "__main__":
    test_agent()