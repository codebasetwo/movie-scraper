import json
import pickle

def load_json(file_path):
    """
    Loads data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        The loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the JSON file is invalid.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON data in '{file_path}': {e}")
        raise

    
def save_json(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except OSError as e:
        print(f"Error: Failed to save data to '{file_path}': {e}")
        raise



def save_pickle(name, data):
    """
    Saves data to a pickle file.

    Args:
        name (str): Path to the pickle file.
        data: The data to be saved.

    Raises:
        OSError: If an error occurs during file writing.
    """
    try:
        with open(name, 'wb') as f:
            pickle.dump(data, f)
    except OSError as e:
        print(f"Error: Failed to save data to '{name}': {e}")
        raise


def load_pickle(name):
    """
    Loads data from a pickle file.

    Args:
        name (str): Path to the pickle file.

    Returns:
        The loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pickle.UnpicklingError: If the pickle file is invalid.
    """
    try:
        with open(name, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: File '{name}' not found.")
        raise
    except pickle.UnpicklingError as e:
        print(f"Error: Invalid pickle data in '{name}': {e}")
        raise



