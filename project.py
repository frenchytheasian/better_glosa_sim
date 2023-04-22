"""
This script runs the project with the necessary configurations to generate the needed
output for my project.
"""
import subprocess
from csv import writer
import os
import time

from output.parse_xml import get_runtime
from output.visualize import visualize


def process_data(
    filename: str, pcc: bool, seed: int, intersections: int, distance: int
):
    """
    Generate output graphs and write total values to a .csv for later processing
    """
    # Attribs to generate:
    attribs = ["speed", "CO2", "fuel", "waiting"]

    path = f"output/{filename}_{'pcc' if pcc else 'normal'}_data.csv"
    if not os.path.exists(path):
        with open(path, "a") as f:
            f.write(f"is_pcc,seed,intersections,distance,time,{','.join(attribs)}\n")

    speed = visualize("speed")
    CO2 = visualize("CO2")
    fuel = visualize("fuel")
    waiting = visualize("waiting")

    with open(path, "a") as f:
        writer_object = writer(f)

        row = [
            pcc,
            seed,
            intersections,
            distance,
            get_runtime(),
            speed,
            CO2,
            fuel,
            waiting,
        ]

        writer_object.writerow(row)

        f.close()


def run(filename: str, pcc: bool, intersections: int, seed: int, distance: int):
    """Run the project with the given configurations

    Args:
        pcc (bool): Whether or not to use pcc
    """

    if pcc:
        completed_process = subprocess.run(
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
        completed_process = subprocess.run(
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

    if completed_process.returncode != 0:
        process_data(filename, pcc, -1, -1, -1)
    else:
        process_data(filename, pcc, seed, intersections, distance)


def main():
    """
    Run the project multiple times with different parameters and calculate their outputs
    """
    start = time.time()

    for i in range(0, 11):
        for j in range(1, 21):
            for k in range(1, 11):
                run("cv2x", pcc=True, intersections=j, seed=i, distance=100 * k)
                run("cv2x", pcc=False, intersections=j, seed=i, distance=100 * k)

    end = time.time()
    print(f"Total time: {end - start}")


if __name__ == "__main__":
    main()
