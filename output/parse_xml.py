import xml.etree.cElementTree as ET
from collections import defaultdict
from typing import Dict, List


def _normalize_values(values: dict) -> dict:
    """normalize the values"""
    max_len = max([len(values[id]) for id in values.keys() if id != "time"])
    values["time"] = values["time"][:max_len]

    for id in values.keys():
        values[id] = values[id] + [values[id][-1]] * (max_len - len(values[id]))
    return values


def _get_value_from_data(data: ET.Element, attrib: str) -> str:
    """get the value of an attribute from the xml <data> element"""
    all_values = []
    for vehicle in data.find("vehicles"):
        all_values.append((vehicle.attrib["id"], vehicle.attrib[attrib]))
    return all_values


def get_runtime() -> int:
    """Parse the full.xml file for the runtime

    Returns:
        int: The runtime
    """
    tree = ET.parse("output/full.xml")
    root = tree.getroot()
    return int(root[-1].attrib["timestep"])


def get_vehicle_attrib(attrib: str) -> Dict[str, List]:
    """Parse the full.xml file for the values of a given attribute

    Args:
        attrib (str): The attribute to parse for

    Returns:
        Dict[List]: A dictionary with the vehicle id as key and a list of values
    """
    tree = ET.parse("output/full.xml")
    root = tree.getroot()

    values = defaultdict(list)
    for data in root:
        all_values = _get_value_from_data(data, attrib)
        for value in all_values:
            id, attrib_val = value
            values[id].append(int(float(attrib_val)))

        values["time"].append(int(float(data.attrib["timestep"])))
    values = _normalize_values(values)

    return values
