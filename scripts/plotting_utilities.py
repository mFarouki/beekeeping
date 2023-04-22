import pathlib

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.path import Path
from matplotlib.textpath import TextToPath

from scripts.constants import PRIMARY_DATE_COL

SYMBOLA_PATH = r"C:\Users\milly\AppData\Local\Microsoft\Windows\Fonts\Symbola-AjYx.ttf"
SYMBOLS = {"bee": "\U0001F41D"}
font_properties = fm.FontProperties(fname=SYMBOLA_PATH)


def partition_colormap(colormap_name: str, n_partitions: int):
    colormap = plt.get_cmap(colormap_name)
    colormap_list = [colormap(i) for i in range(colormap.N)]
    partition_step = round((colormap.N - 1) / n_partitions)
    return [colormap_list[n] for n in range(0, colormap.N - 1, partition_step)]


def get_marker_as_path(symbol):
    v, codes = TextToPath().get_text_path(font_properties, symbol)
    v = np.array(v)
    mean = np.mean([np.max(v, axis=0), np.min(v, axis=0)], axis=0)
    return Path(v - mean, codes, closed=False)


def plot_numerical_data(
    dataframe: pd.DataFrame, hive: str, title: str, output_directory: pathlib.Path
):
    hive_df = dataframe[dataframe["hive"].str.lower() == hive.lower()]
    numerical_values = hive_df.select_dtypes(include=np.number)
    colormap = partition_colormap("Wistia", numerical_values.shape[1])

    ax = None
    plot_count = 0

    for integer_field in numerical_values.columns:
        shared_arguments = {
            "kind": "scatter",
            "x": PRIMARY_DATE_COL,
            "y": integer_field,
            "s": 50 * numerical_values[integer_field],
            "color": colormap[plot_count],
            "label": integer_field,
            "marker": get_marker_as_path(SYMBOLS["bee"]),
        }
        if ax is None:
            ax = hive_df.plot(**shared_arguments)
        else:
            hive_df.plot(ax=ax, **shared_arguments)
        plot_count += 1
    ax.legend(loc="upper left")
    plt.xticks(rotation=45)
    plt.ylabel("count")
    plt.title(f"{title} for {hive.title()}")
    plt.tight_layout()
    plt.savefig(output_directory / f"{hive}_{title}.png")
