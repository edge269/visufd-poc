"""
DataSet Module

Provides DataSet class for loading CSV data into a pandas DataFrame.
"""

from pathlib import Path
import pandas as pd
from typing import Optional, Dict


class DataSet:
    """
    DataSet for loading CSV data files into pandas DataFrames.
    """
    # Instance attributes
    df: Optional[pd.DataFrame]
    type_data: str

    # Optional mapping of column names to subtypes ('position','cell','face')
    def __init__(self, filepath: Path, type_data: str = 'grid', pairing_dictionary: Optional[Dict[str, str]] = None):
        """
        Initializes the DataSet.

        Args:
            filepath (Path): Path to the data CSV file.
            type_data (str): Type of data to load (e.g., 'grid').
            pairing_dictionary (Dict[str,str], optional): Map of column names to subtypes.
        """
        # Normalize path
        self.filepath = filepath.resolve()
        # Placeholder for loaded DataFrame
        self.df = None
        # Data type specifier
        self.type_data = type_data
        # Column subtype mapping
        self.pairing_dictionary = pairing_dictionary or {}
    
    def load(self, filepath: Optional[Path] = None) -> pd.DataFrame:
        """
        Loads the CSV file into a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the CSV data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or cannot be parsed.
        """
        # If a new filepath is provided at load-time, override
        if filepath is not None:
            self.filepath = filepath.resolve()
        # Validate supported data types
        if self.type_data != 'grid':
            raise ValueError(f"Unsupported type_data: {self.type_data}")
        if not self.filepath.exists():
            raise FileNotFoundError(f"Data file not found: {self.filepath}")
        try:
            df = pd.read_csv(self.filepath)
        except pd.errors.EmptyDataError:
            raise ValueError(f"No data found in file: {self.filepath}")
        except Exception as e:
            raise ValueError(f"Failed to load data from {self.filepath}: {e}")
        # Validate pairing dictionary against DataFrame
        self._validate_pairing(df)
        # Store loaded DataFrame and mapping
        self.df = df
        return self.df
    
    def _validate_pairing(self, df: pd.DataFrame) -> None:
        """
        Internal validation of pairing_dictionary:
         - must include exactly one 'position'
         - subtypes must be in {'position','cell','face'}
         - keys must exist in df.columns
        """
        allowed = {'position', 'cell', 'face'}
        pos_count = 0
        for col, subtype in self.pairing_dictionary.items():
            if col not in df.columns:
                raise KeyError(f"Column '{col}' not found in data")
            if subtype not in allowed:
                raise ValueError(f"Invalid subtype '{subtype}' for column '{col}'")
            if subtype == 'position':
                pos_count += 1
        if pos_count != 1:
            raise ValueError("pairing_dictionary must contain exactly one column mapped to 'position'")
    
    def __repr__(self) -> str:
        """Return an unambiguous representation of the DataSet."""
        # Describe filepath, data type, and load status
        status = f"{len(self.df)} rows" if self.df is not None else "not loaded"
        return (f"<DataSet(filepath={self.filepath!r}, "
                f"type_data={self.type_data!r}, loaded={status!r})>")

    def __str__(self) -> str:
        """Human-readable summary of the loaded DataFrame."""
        if self.df is not None:
            rows, cols = self.df.shape
            col_list = list(self.df.columns)
            return (
                f"DataSet({self.filepath.name!r}): {rows} rows, {cols} columns\n"
                f"Columns: {col_list}"
            )
        return f"DataSet({self.filepath.name!r}) not loaded. Call load() first."
