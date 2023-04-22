"""
This script runs the project with the necessary configurations to generate the needed
output for my project.
"""
import subprocess
from pathlib import Path
from csv import writer

from output.parse_xml import get_runtime
from output.visualize import visualize


def process_data(pcc: bool, seed: int, intersections: int):
    """
    Generate output graphs and write total values to a .csv for later processing
    """
    # Attribs to generate:
    attribs = ["speed", "CO2"]

    path = Path("outptut/sim_data.csv")
    if not path.exists():
        with open("output/sim_data.csv", "w") as f:
            f.write(f"is_pcc,seed,intersections,time,{','.join(attribs)}\n")

    speed = visualize("speed")
    CO2 = visualize("CO2")

    with open("output/sim_data.csv", "a") as f:
        writer_object = writer(f)

        row = [pcc, seed, intersections, get_runtime(), speed, CO2]

        writer_object.writerow(row)

        f.close()


def run(pcc: bool, intersections: int, seed: int):
    """Run the project with the given configurations

    Args:
        pcc (bool): Whether or not to use pcc
    """

    if pcc:
        subprocess.run(
            [
                "python",
                "runner.py",
                "--pcc",
                "--nogui",
                "--seed",
                str(seed),
                "--intersections",
                str(intersections),
            ]
        )
    else:
        subprocess.run(
            [
                "python",
                "runner.py",
                "--nogui",
                "--seed",
                str(seed),
                "--intersections",
                str(intersections),
            ]
        )

    process_data(pcc, seed, intersections)


def main():
    """
    Run the project multiple times with different parameters and calculate their outputs
    """
    run(True, 20, 0)
    run(False, 20, 0)


if __name__ == "__main__":
    main()
