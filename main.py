"""
main.py

Main entry point for the CSV Query and Visualization Application.
This script imports the Gradio-based frontend interface and launches the application.
"""

from frontend import demo

def main():
    """
    Launches the Gradio application.
    """
    demo.launch()

if __name__ == "__main__":
    main()
