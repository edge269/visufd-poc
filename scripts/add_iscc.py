#!/usr/bin/env python3
"""
Command-line tool to add randomized iscc1–iscc4 faces to a grid CSV.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def generate_iscc_dataframe(rows: int) -> pd.DataFrame:
    """
    Generate a DataFrame with iscc1..iscc4, two random ints [1..5] per row, NaN elsewhere.
    """
    data = []
    for _ in range(rows):
        row = [np.nan] * 4
        choices = np.random.choice(4, size=2, replace=False)
        for i in choices:
            row[i] = np.random.randint(1, 6)
        data.append(row)
    return pd.DataFrame(data, columns=[f'iscc{i}' for i in range(1, 5)])


def main():
    parser = argparse.ArgumentParser(
        description='Add iscc1–iscc4 columns to a grid CSV, with two random face values per row.'
    )
    parser.add_argument(
        'input_csv',
        type=Path,
        help='Path to input CSV file (e.g., data/grid_random.csv)'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Path to write output CSV (defaults to overwrite input)'
    )
    args = parser.parse_args()

    csv_path = args.input_csv.resolve()
    if not csv_path.exists():
        print(f"Error: input file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to load CSV: {e}", file=sys.stderr)
        sys.exit(1)

    iscc_df = generate_iscc_dataframe(len(df))
    df = pd.concat([df, iscc_df], axis=1)

    output_path = args.output.resolve() if args.output else csv_path
    try:
        df.to_csv(output_path, index=False)
    except Exception as e:
        print(f"Failed to write CSV: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Written {len(df)} rows with iscc1..iscc4 to {output_path}")


if __name__ == '__main__':
    main()
