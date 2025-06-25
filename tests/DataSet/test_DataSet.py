import pytest
import pandas as pd
from pathlib import Path
from src.DataSet import DataSet


def write_csv(path: Path, content: str):
    path.write_text(content)


def test_load_valid_csv(tmp_path):
    # Create a sample CSV file
    csv_content = """position,cell_value,face1,face2\nA1,10,0.1,0.2\nB2,20,0.3,0.4"""
    csv_file = tmp_path / "sample.csv"
    write_csv(csv_file, csv_content)

    ds = DataSet(csv_file)
    df = ds.load()
    # Check DataFrame is loaded and attribute set
    assert isinstance(df, pd.DataFrame)
    assert ds.df is df
    # Check values
    assert list(df.columns) == ["position", "cell_value", "face1", "face2"]
    assert df.shape == (2, 4)
    assert df.loc[0, "position"] == "A1"
    assert df.loc[1, "cell_value"] == 20
    # __repr__ and __str__ before and after load
    ds2 = DataSet(csv_file)
    rep = repr(ds2)
    assert "not loaded" in rep
    s = str(ds2)
    assert "not loaded" in s

    # after loading
    ds2.load()
    rep2 = repr(ds2)
    assert "loaded='2 rows'" in rep2
    s2 = str(ds2)
    assert "2 rows, 4 columns" in s2
    assert "position" in s2 and "cell_value" in s2


def test_load_override_filepath(tmp_path):
    # Create two CSVs: one valid, one with different content
    csv1 = tmp_path / "one.csv"
    csv2 = tmp_path / "two.csv"
    write_csv(csv1, """pos,val\nX,1""")
    write_csv(csv2, """pos,val\nY,2\nZ,3""")
    ds = DataSet(csv1)
    # override filepath at load time to csv2
    df2 = ds.load(csv2)
    assert df2.shape == (2, 2)
    assert ds.df is df2


def test_file_not_found(tmp_path):
    missing = tmp_path / "no.csv"
    ds = DataSet(missing)
    with pytest.raises(FileNotFoundError):
        ds.load()


def test_empty_csv(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    ds = DataSet(empty_file)
    with pytest.raises(ValueError) as excinfo:
        ds.load()
    assert "No data found in file" in str(excinfo.value)


def test_unsupported_type_data(tmp_path):
    # Create a valid CSV but pass unsupported type_data
    csv_content = """position,cell_value\nX,1"""
    csv_file = tmp_path / "grid.csv"
    write_csv(csv_file, csv_content)

    ds = DataSet(csv_file, type_data='other')
    with pytest.raises(ValueError) as excinfo:
        ds.load()
    assert "Unsupported type_data" in str(excinfo.value)
