from datetime import datetime
import os

from matplotlib import pyplot as plt

from output.parse_xml import get_vehicle_attrib


def visualize(attrib: str):
    """visualize the attribute"""
    val = get_vehicle_attrib(attrib)
    time = val["time"]
    del val["time"]

    for id, values in val.items():
        plt.plot(time, values, label=id)

    plt.xlabel("timestep")
    plt.ylabel(attrib)
    plt.title(f"{attrib} over time")
    plt.legend()

    if not os.path.exists("graphs"):
        os.mkdir("graphs")

    now = datetime.now()
    now = now.strftime("%d%m%Y%H%M%S")
    plt.savefig(f'graphs/{attrib}-{now}.png')
