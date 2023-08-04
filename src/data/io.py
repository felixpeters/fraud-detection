from pathlib import Path

import pandas as pd


def load_dataframes(directory: Path, start_date: str = None, end_date: str = None, sort_by: str = None) -> pd.DataFrame:
    """Loads dataframes from a directory of pickle files. Assumes filenames to be in the format YYYY-MM-DD.pkl.

    Args:
        directory (Path): Directory containing pickle files.
        start_date (str, optional): Start date. Defaults to None, which takes all files from the start.
        end_date (str, optional): End date. Defaults to None, which takes all files until the end.
        sort_by (str, optional): Columns to sort combined dataframe by. Defaults to None.

    Returns:
        pd.DataFrame: (Sorted) combined dataframe.
    """
    # Get a list of all files in the directory
    files = sorted(directory.glob("*.pkl"))

    # Filter files based on start and end dates
    if start_date is not None:
        files = [f for f in files if f >= start_date]
    if end_date is not None:
        files = [f for f in files if f <= end_date]

    # Load dataframes from files
    dataframes = []
    for file in files:
        with open(file, "rb") as f:
            dataframes.append(pd.read_pickle(f))

    # Combine dataframes into one dataframe
    combined_dataframe = pd.concat(dataframes)

    # Sort dataframe by datetime column if sort_by is specified
    if sort_by is not None:
        combined_dataframe.sort_values(by=sort_by, inplace=True)

    return combined_dataframe
