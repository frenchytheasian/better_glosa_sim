from matplotlib import pyplot as plt

from output.parse_xml import get_vehicle_attrib


def visualize(attrib: str):
    """visualize the attribute"""
    val = get_vehicle_attrib(attrib)
    time = val["time"]
    del val["time"]

    for id, values in val.items():
        print(values)
        plt.plot(time, values, label=id)
    plt.legend()
    plt.show()
