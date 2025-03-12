import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from .template.schema import FilterResult
import yaml

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Access agent configurations
agent_model = config["Agent"]["model_name"]
base_url = config["Agent"]["base_url"]

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

# Initialize the Ollama model using llama3.2 (2.0GB) as specified
ollama_model = OpenAIModel(
    model_name=agent_model,
    provider=OpenAIProvider(base_url=base_url)
)

# Initialize the Agent with the model, dependency type, expected result type, and system prompt
agent = Agent(
    ollama_model,
    deps_type=list[str],
    result_type=FilterResult,
    system_prompt=system_prompt,
    retries=2
)

@agent.tool
async def get_column_names(ctx: RunContext[list[str]]) -> str:
    """
    Agent tool to retrieve column names from the provided list of dependencies.
    Joins the column names into a comma-separated string.
    
    Parameters:
        ctx (RunContext[list[str]]): The context containing a list of column names.
    
    Returns:
        str: Comma-separated column names.
    """
    return ', '.join(ctx.deps)