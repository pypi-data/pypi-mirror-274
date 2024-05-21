# hyperdyn/data_handling.py

import pandas as pd

def load_data(file_path):
    """
    Load data from a file.

    Parameters:
    file_path (str): Path to the input file.

    Returns:
    pd.DataFrame: Loaded data.
    """
    return pd.read_csv(file_path)

def preprocess_data(data):
    """
    Preprocess the loaded data.

    Parameters:
    data (pd.DataFrame): Input data to preprocess.

    Returns:
    pd.DataFrame: Preprocessed data.
    """
    # Perform data preprocessing steps
    data.fillna(data.mean(), inplace=True)
    data = data.drop_duplicates()
    return data

def save_data(data, file_path):
    """
    Save data to a file.

    Parameters:
    data (pd.DataFrame): Data to be saved.
    file_path (str): Path to the output file.
    """
    data.to_csv(file_path, index=False)

# Public function to expose data handling functionalities
def main():
    """
    Entry point for data handling functionalities.
    """
    # Example usage
    input_file = "input_data.csv"
    output_file = "preprocessed_data.csv"

    # Load data
    data = load_data(input_file)

    # Preprocess data
    preprocessed_data = preprocess_data(data)

    # Save preprocessed data
    save_data(preprocessed_data, output_file)
