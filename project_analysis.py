from pathlib import Path
from typing import Tuple, Dict
from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt


def compare_totals(normal: int, cv2x: int, dsrc: int) -> Tuple[float, float]:
    """Compare the totals of the given attributes

    Args:
        normal (int): Total of the attribute for normal
        cv2x (int): Total of the attribute for cv2x
        dsrc (int): Total of the attribute for dsrc

    Returns:
        Tuple[float, float]: Percentage difference between normal and cv2x, Percentage
        difference between normal and dsrc
    """
    cv2x_diff = (normal - cv2x) / cv2x
    dsrc_diff = (normal - dsrc) / dsrc
    dsrc_cv2x_diff = (cv2x - dsrc) / dsrc

    return cv2x_diff, dsrc_diff, dsrc_cv2x_diff


def compare_all_totals(normal: Dict, cv2x: Dict, dsrc: Dict) -> Dict:
    """Compare the totals of all the attributes

    Args:
        normal (Dict): Dictionary of the totals for normal
        cv2x (Dict): Dictionary of the totals for cv2x
        dsrc (Dict): Dictionary of the totals for dsrc

    Returns:
        Dict: Dictionary of the percentage differences
    """
    attribs = ["speed", "CO2", "fuel", "waiting", "time"]

    diffs = {}
    for attrib in attribs:
        cv2x_diff, dsrc_diff, dsrc_cv2x_diff = compare_totals(
            normal[attrib], cv2x[attrib], dsrc[attrib]
        )
        diffs[attrib] = {
            "cv2x": cv2x_diff,
            "dsrc": dsrc_diff,
            "dsrc_cv2x": dsrc_cv2x_diff,
        }

    return diffs


def get_total(df: pd.DataFrame, attrib: str) -> Tuple[int, int, int]:
    """Get the total of the given attribute

    Args:
        df (pd.DataFrame): Merged dataframe
        attrib (str): Attribute to get the total of

    Returns:
        int: total of the attribute for normal
        int: total of the attribute for pcc
    """
    normal = df[f"normal_{attrib}"].sum()
    cv2x = df[f"cv2x_{attrib}"].sum()
    dsrc = df[f"dsrc_{attrib}"].sum()

    return normal, cv2x, dsrc


def get_all_totals(df: pd.DataFrame) -> Dict:
    """Get the total of all the attributes

    Args:
        df (pd.DataFrame): Merged dataframe

    Returns:
        Dict: Dictionary of the totals
    """
    attribs = ["speed", "CO2", "fuel", "waiting", "time"]

    totals = defaultdict(dict)
    for attrib in attribs:
        normal, cv2x, dsrc = get_total(df, attrib)
        totals["normal"][attrib] = normal
        totals["cv2x"][attrib] = cv2x
        totals["dsrc"][attrib] = dsrc

    return totals


def get_averages_df(df: pd.DataFrame) -> pd.DataFrame:
    """The dataframes have a seed, intersection, and distance column. This finds the
    average of different seeds given all the other parameters are equal. If
    intersection, and distance are equal, then find the average of the seeds.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Output dataframe
    """
    return df.groupby(["is_pcc", "intersections", "distance"]).mean().reset_index()


def bar_plot_diffs(diffs: dict) -> None:
    """Plot the percentage differences

    Args:
        diffs (dict): Dictionary of the percentage differences
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # attribs = ["CO2", "fuel", "time"]
    attribs = ["waiting"]
    cv2x_diffs = [diffs[attrib]["cv2x"] for attrib in attribs]
    dsrc_diffs = [diffs[attrib]["dsrc"] for attrib in attribs]
    dsrc_cv2x_diffs = [diffs[attrib]["dsrc_cv2x"] for attrib in attribs]

    x = [i for i in range(len(attribs))]
    width = 0.25

    ax.bar(x, cv2x_diffs, width, label="CV2X")
    ax.bar([i + width for i in x], dsrc_diffs, width, label="DSRC")
    ax.bar([i + width * 2 for i in x], dsrc_cv2x_diffs, width, label="DSRC - CV2X")

    ax.set_ylabel("Percentage Difference")
    ax.set_title("Percentage Difference of Attributes")
    ax.set_xticks([i + width for i in x])
    ax.set_xticklabels(attribs)
    ax.legend()

    # Add value labels to the bars
    for i, v in enumerate(cv2x_diffs):
        ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")
    for i, v in enumerate(dsrc_diffs):
        ax.text(i + width, v, f"{v:.2f}", ha="center", va="bottom")
    for i, v in enumerate(dsrc_cv2x_diffs):
        ax.text(i + width * 2, v, f"{v:.2f}", ha="center", va="bottom")

    plt.savefig("waiting.png")


def graph_attrib_vs_distance(
    normal_df: pd.DataFrame,
    cv2x_df: pd.DataFrame,
    dsrc_df: pd.DataFrame,
    attrib: str,
    intersections: int,
) -> None:
    """Graph the given attribute vs distance

    Args:
        normal_df (pd.DataFrame): Normal dataframe
        cv2x_df (pd.DataFrame): CV2X dataframe
        dsrc_df (pd.DataFrame): DSRC dataframe
        attrib (str): Attribute to graph
        intersections (int): Number of intersections
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    normal_df = normal_df[normal_df["intersections"] == intersections]
    cv2x_df = cv2x_df[cv2x_df["intersections"] == intersections]
    dsrc_df = dsrc_df[dsrc_df["intersections"] == intersections]

    normal_df = normal_df.sort_values(by=["distance"])
    cv2x_df = cv2x_df.sort_values(by=["distance"])
    dsrc_df = dsrc_df.sort_values(by=["distance"])

    normal = normal_df[f"{attrib}"]
    cv2x = cv2x_df[f"{attrib}"]
    dsrc = dsrc_df[f"{attrib}"]
    distance = normal_df["distance"]

    ax.plot(distance, normal, label="Normal")
    ax.plot(distance, cv2x, label="CV2X")
    ax.plot(distance, dsrc, label="DSRC")

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel(attrib)
    ax.set_title(f"{attrib} vs Distance")
    ax.legend()

    plt.savefig(f"{attrib}_vs_distance_{intersections}.png")


def graph_attrib_vs_intersections(
    normal_df: pd.DataFrame,
    cv2x_df: pd.DataFrame,
    dsrc_df: pd.DataFrame,
    attrib: str,
    distance: int,
) -> None:
    """Graph the given attribute vs intersections

    Args:
        normal_df (pd.DataFrame): Normal dataframe
        cv2x_df (pd.DataFrame): CV2X dataframe
        dsrc_df (pd.DataFrame): DSRC dataframe
        attrib (str): Attribute to graph
        distance (int): Distance
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    normal_df = normal_df[normal_df["distance"] == distance]
    cv2x_df = cv2x_df[cv2x_df["distance"] == distance]
    dsrc_df = dsrc_df[dsrc_df["distance"] == distance]

    normal_df = normal_df.sort_values(by=["intersections"])
    cv2x_df = cv2x_df.sort_values(by=["intersections"])
    dsrc_df = dsrc_df.sort_values(by=["intersections"])

    normal = normal_df[f"{attrib}"]
    cv2x = cv2x_df[f"{attrib}"]
    dsrc = dsrc_df[f"{attrib}"]
    intersections = normal_df["intersections"]

    ax.plot(intersections, normal, label="Normal")
    ax.plot(intersections, cv2x, label="CV2X")
    ax.plot(intersections, dsrc, label="DSRC")

    ax.set_xlabel("Intersections")
    ax.set_ylabel(attrib)
    ax.set_title(f"{attrib} vs Intersections")
    ax.legend()

    plt.savefig(f"{attrib}_vs_intersections_{distance}.png")


def main():
    normal_file = Path("cv2x_normal_data.csv")
    cv2x_file = Path("cv2x_pcc_data.csv")
    dsrc_file = Path("dsrc_pcc_data.csv")

    normal_df = pd.read_csv(normal_file)
    cv2x_df = pd.read_csv(cv2x_file)
    dsrc_df = pd.read_csv(dsrc_file)

    # Get the averages of the dataframes
    normal_avg_df = get_averages_df(normal_df)
    cv2x_avg_df = get_averages_df(cv2x_df)
    dsrc_avg_df = get_averages_df(dsrc_df)

    # Change the column names to differ and merge the dataframes
    normal_avg_df.columns = [f"normal_{col}" for col in normal_avg_df.columns]
    cv2x_avg_df.columns = [f"cv2x_{col}" for col in cv2x_avg_df.columns]
    dsrc_avg_df.columns = [f"dsrc_{col}" for col in dsrc_avg_df.columns]

    merged_df = pd.concat([normal_avg_df, cv2x_avg_df], axis=1)
    merged_df = pd.concat([merged_df, dsrc_avg_df], axis=1)

    totals = get_all_totals(merged_df)
    diffs = compare_all_totals(totals["normal"], totals["cv2x"], totals["dsrc"])
    bar_plot_diffs(diffs)

    distance = 100

    for attrib in ["CO2", "fuel", "time", "waiting"]:
        graph_attrib_vs_intersections(
            get_averages_df(normal_df),
            get_averages_df(cv2x_df),
            get_averages_df(dsrc_df),
            attrib,
            distance,
        )


if __name__ == "__main__":
    main()
