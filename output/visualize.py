from datetime import datetime
import os

from matplotlib import pyplot as plt

from output.parse_xml import get_vehicle_attrib


def visualize(attrib: str):
    """visualize the attribute"""
    response = get_vehicle_attrib(attrib)
    val = response[0]
    time = val["time"]
    del val["time"]

    values = list(val.values())[0]
    if attrib == "waiting":
        total = sum(
            [
                wait
                for i, wait in enumerate(values)
                if i == len(values) - 1 or values[i + 1] == 0
            ]
        )
    else:
        total = sum(values)
    car = ""
    for id, values in val.items():
        plt.plot(time, values, label=id)
        car = id

    plt.xlabel("timestep")
    plt.ylabel(attrib)
    plt.title(f"{attrib} over time")
    plt.legend()

    if not os.path.exists("graphs"):
        os.mkdir("graphs")

    now = datetime.now()
    now = now.strftime("%Y%m%d%H%M%S")
    plt.savefig(f"graphs/{attrib}-{car}-{now}.png")

    return total
