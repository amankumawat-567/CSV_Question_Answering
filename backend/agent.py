import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.cohere import CohereModel
import yaml

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Access agent configurations
agent_model = config["Agent"]["model_name"]
api_key = config["Agent"]["api_key"]

global system_prompt

def load_system_prompt(file_path: str = os.path.join(os.path.dirname(__file__), "template\system_prompt.txt")) -> str:
    """
    Loads the system prompt from the specified file path.

    Parameters:
        file_path (str): The path to the system prompt file.

    Returns:
        str: The content of the system prompt.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Load system prompt from file
system_prompt = load_system_prompt()

# Model
Cohere_model = CohereModel(agent_model,api_key=api_key)

# Initialize the Agent with the model, dependency type, expected result type, and system prompt
agent = Agent(
    Cohere_model,
    deps_type=list[str],
    result_type= str,
    retries=2
)

@agent.system_prompt
async def get_system_prompt(ctx: RunContext[list[str]]) -> str:
    """
    Agent tool to retrieve column names from the provided list of dependencies.
    
    Parameters:
        ctx (RunContext[list[str]]): The context containing a list of column names.
    
    Returns:
        list[str]: A list of column names.
    """
    prompt = system_prompt.replace("[COLUMN_NAMES]",', '.join(ctx.deps))
    
    return prompt