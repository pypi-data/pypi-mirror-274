# hyperdyn/utils.py

import os
import shutil

def create_directory(directory_path):
    """
    Create a new directory.

    Parameters:
    directory_path (str): Path to the directory to be created.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

def copy_file(source_path, destination_path):
    """
    Copy a file from source to destination.

    Parameters:
    source_path (str): Path to the source file.
    destination_path (str): Path to the destination directory.
    """
    shutil.copy2(source_path, destination_path)
    print(f"File '{source_path}' copied to '{destination_path}'.")

def get_config_path():
    """
    Get the path to the configuration file.

    Returns:
    str: Path to the configuration file.
    """
    config_dir = os.path.expanduser("~/.hyperdyn")
    config_file = os.path.join(config_dir, "config.ini")
    return config_file

# Public function to expose utility functionalities
def main():
    """
    Entry point for utility functionalities.
    """
    # Example usage
    directory_path = "path/to/new_directory"
    create_directory(directory_path)

    source_file = "path/to/source_file.txt"
    destination_dir = "path/to/destination_directory"
    copy_file(source_file, destination_dir)

    # Get the path to the configuration file
    config_path = get_config_path()
    print(f"Configuration file path: {config_path}")
