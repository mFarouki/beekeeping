import os
import pathlib

import click
import pandas as pd
from constants import (DATE_COLS, HIVE, HIVES, INSPECTION_HEADER,
                       PRIMARY_DATE_COL, TEMPERAMENT)
from matplotlib.path import Path
from plotting_utilities import plot_numerical_data

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
FRAME_KEYWORDS = ["dn4", "sn4"]
IMAGES_PATH = pathlib.Path(SCRIPT_PATH) / "imgs"
IMAGES_PATH.mkdir(exist_ok=True)


def read_data(filepath: Path) -> pd.DataFrame:
    return pd.read_csv(
        filepath,
        dtype=INSPECTION_HEADER,
        parse_dates=DATE_COLS,
        infer_datetime_format=True,
    )


def check_data(df: pd.DataFrame) -> None:
    assert (
        df[TEMPERAMENT].between(1, 5).all()
    ), "all temperament values must be between 1 (worst) and 5 (best)"
    assert (
        df[HIVE].str.lower().isin(HIVES).all()
    ), f"hives must be one of: {', '.join(HIVES)}"


@click.command()
@click.option(
    "--data",
    type=click.Path(),
    default=pathlib.Path("../data/sample_hive_inspection.csv"),
)
def interpret_inspection_data(data):
    df = read_data(data)
    check_data(df)
    frame_data = [
        column
        for column in df.columns
        if any(keyword in column for keyword in FRAME_KEYWORDS)
    ]
    frame_data.extend([PRIMARY_DATE_COL, HIVE])
    plot_numerical_data(df[frame_data], IMAGES_PATH)


if __name__ == "__main__":
    interpret_inspection_data()
