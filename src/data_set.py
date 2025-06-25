"""
DataSet Module

Provides DataSet class for loading CSV data into a pandas DataFrame.
"""

from pathlib import Path
import pandas as pd


class DataSet:
    """
    DataSet for loading CSV data files into pandas DataFrames.
    """
    def __init__(self, filepath: Path):
        """
        Initializes the DataSet.

        Args:
            filepath (Path): Path to the data CSV file.
        """
        # Normalize path
        self.filepath = filepath.resolve()
    
    def load(self) -> pd.DataFrame:
        """
        Loads the CSV file into a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the CSV data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or cannot be parsed.
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Data file not found: {self.filepath}")
        try:
            df = pd.read_csv(self.filepath)
        except pd.errors.EmptyDataError:
            raise ValueError(f"No data found in file: {self.filepath}")
        except Exception as e:
            raise ValueError(f"Failed to load data from {self.filepath}: {e}")
        return df
