import polars as pl

def load_csv(file_path):
    """
    Load CSV file into a Polars DataFrame

    Args:
        file_path (str): Path tp CSV file

    Returns:
        pl.DataFrame
    """

    df = pl.scan_csv(file_path)
    return df