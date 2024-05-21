# hyperdyn/__init__.py

__version__ = "0.1.0"

# Import and expose the public functions or classes from the package
from .utils import useful_function, another_useful_function
from .data_handling import load_data, preprocess_data
from .cli import command_line_tool

# Public classes or functions defined directly in the package
class HyperdynTool:
    def __init__(self, config):
        self.config = config

    def perform_action(self):
        # Implement the action performed by the tool
        pass

# Public function defined directly in the package
def perform_calculation(a, b):
    # Implement the calculation logic
    return a * b
