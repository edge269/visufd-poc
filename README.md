# FA Grid Data Visualization Project

This project provides tools for visualizing fuel assembly (FA) grid-level data at the rod level.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Data

Place your grid data CSV in the `data/` folder (e.g., `data/grid_random.csv`).

## Usage

Use the `DataSet` class to load data into a pandas DataFrame:

```python
from pathlib import Path
from src.data_set import DataSet

# Initialize DataSet with path to CSV file
dataset = DataSet(Path('data/grid_random.csv'))

# Load data into DataFrame
df = dataset.load()
print(df.head())
```

Columns are retained as in the CSV: `position`, `cell_value`, `face1`–`face4`.

## Visualization

Further visualization tools can be found in `src/visualizer.py` to create 2D grid plots of cell and face values.
