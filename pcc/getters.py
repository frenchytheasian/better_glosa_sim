from typing import List, Dict
import xml.etree.cElementTree as ET

import traci

#################
### GET STATE ###
#################
def _get_vehicle_state(vehicle: str, tls: dict):
    state = {}

    state['position'] = traci.vehicle.getPosition(vehicle)
    state['current_road'] = traci.vehicle.getRoadID(vehicle)

    state['upcoming_tls'] = []
    for id, tl in tls.items():
        if state['position'][0] < tl[0]:
            state['upcoming_tls'].append({id: tl[0] - state['position'][0]})

    state['speed'] = traci.vehicle.getSpeed(vehicle)
    state['id'] = vehicle

    return state

def _get_tl_position():
    """get the position of the traffic lights"""
    tl_positions = {}
    for tl in traci.trafficlight.getIDList():
        tl_positions[tl] = traci.junction.getPosition(tl)
    
    return tl_positions

def get_state():
    """get the state of the simulation"""
    vehicles = traci.vehicle.getIDList()

    states = {}
    tl_positions = _get_tl_position()
    for vehicle in vehicles:
        state = _get_vehicle_state(vehicle, tl_positions)
        states[vehicle] = state

    return states

##################################
### GET STATIC SIGNAL SCHEDULE ###
##################################
def _get_single_schedule(tlLogic: ET.Element) -> List[int]:
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
        schedule = _get_single_schedule(tlLogic)
        schedules[tlLogic.attrib['id']] = schedule
    
    return schedules