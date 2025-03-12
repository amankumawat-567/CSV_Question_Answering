"""
Backend package for the CSV Query and Visualization Application.

Modules:
- agent: Configures the LLM agent and loads the system prompt.
- csv_handler: Handles CSV file loading and validation.
- filter_executor: Executes filtering scripts and prepares visualizations.
"""

from .agent import agent
from .csv_handler import load_csv, validate_csv
from .filter_executor import execute_filter_script, plot_graph