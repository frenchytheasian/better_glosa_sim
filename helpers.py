import xml.etree.cElementTree as ET
from typing import List, Dict

def _get_singal_schedule(tlLogic: ET.Element) -> List[int]:
    """get the signal schedule
    
    The description of the schedule is as follows:
    [time until the first green, time until the first red, time until the second green, time until the second red, ...]
    """
    N = 1100
    phases = tlLogic.findall("phase")
    schedule = []
    r = int(phases[0].attrib['duration']) if phases[0].attrib['state'] == 'r' else int(phases[1].attrib['duration'])
    g = int(phases[0].attrib['duration']) if phases[0].attrib['state'] == 'G' else int(phases[1].attrib['duration'])

    current = 0 if phases[0].attrib['state'] == 'G' else int(phases[0].attrib['duration'])
    while current < N:
        schedule.append(current)
        current += g
        schedule.append(current)
        current += r
    
    return schedule

def get_static_signal_schedule(name: str) -> Dict[str, List[int]]:
    """get the static signal schedule"""
    tree = ET.parse(f"data/{name}.add.xml")
    tlLogics = tree.findall("tlLogic")

    schedules = {}
    for tlLogic in tlLogics:
        schedule = _get_singal_schedule(tlLogic)
        schedules[tlLogic.attrib['id']] = schedule
    
    return schedules
        

if __name__ == "__main__":
    print(get_static_signal_schedule('test'))