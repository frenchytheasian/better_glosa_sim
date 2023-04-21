from typing import List, Tuple, Dict

import traci


####################
### Adjust Speed ###
####################
def _get_speed_bounds(vehicle_info: dict) -> Tuple[float, float]:
    """get the speed bounds of the vehicle

    This is currently a simplified version of the speed bounds.
    """
    min_v = 1.0
    max_v = traci.vehicle.getAllowedSpeed(vehicle_info["id"])
    return min_v, max_v


def _get_v_bound_for_tl(
    tl: Dict[str, int], tl_schedules: dict, env_v_bound: Tuple[int, int]
) -> Tuple[float, float]:
    """
    Get the velocity bounds to hit green at a specific traffic light

    Args:
        tl (dict): traffic light
        tl_schedules (dict): traffic light schedules
        env_v_bound (tuple): environment velocity bounds
    """
    time = traci.simulation.getTime()
    id, distance = tl.popitem()
    tl_schedule = [x - time for x in tl_schedules[id]]

    for i in range(0, len(tl_schedule), 2):
        if tl_schedule[i + 1] <= 0:
            continue

        v_low = distance / tl_schedule[i + 1]
        if tl_schedule[i] <= 0:
            v_high = float("inf")
        else:
            v_high = distance / tl_schedule[i]

        if not v_low <= env_v_bound[1] and v_high >= env_v_bound[0]:
            continue
        else:
            return max(v_low, env_v_bound[0]), min(v_high, env_v_bound[1])


def _get_target_speed(
    upcoming_tls: List[dict], tl_schedules: dict, env_v_bound: Tuple[float, float]
) -> float:
    """
    get the target speed of the vehicle

    Args:
        upcoming_tls (list): upcoming traffic lights
        tl_schedules (dict): traffic light schedules
        env_v_bound (tuple): environment velocity bounds
    """
    valid_bounds = {}
    for tl in upcoming_tls:
        key = list(tl.keys())[0]
        valid_bound = _get_v_bound_for_tl(tl, tl_schedules, env_v_bound)
        valid_bounds[key] = valid_bound

    # Loop through the valid bounds for each traffic light and find the speed
    # that is valid to pass all traffic lights at green. If this cannot be found, 
    # try to find the speed that is valid to pass through all traffic lights
    # except the last one. Repeat this until a valid speed is found.
    intersection = set()
    for i in range(len(valid_bounds)):
        ranges = [
            set(range(int(x[0] * 10), int(x[1] * 10)))
            for x in list(valid_bounds.values())[: len(valid_bounds) - i]
        ]
        intersection = set.intersection(*ranges)
        if len(intersection) > 0:
            break
    
    valid_speeds = [x / 10.0 for x in intersection]

    if len(valid_speeds) == 0:
        return -1
    
    # current_speed = traci.vehicle.getSpeed(traci.vehicle.getIDList()[0])
    # if current_speed > valid_speeds[0] and current_speed < valid_speeds[-1]:
    #     return current_speed

    return max(valid_speeds)


def adjust_speed(vehicle_info: dict, tl_schedules: dict):
    """Adjust the speed of the vehicle to optimal speed

    Args:
        vehicle_info (dict): A dictionary containing the vehicle information
        tl_schedules (dict): A dictionary containing the traffic light schedules
    """
    speed_bounds = _get_speed_bounds(vehicle_info)
    target_speed = _get_target_speed(
        vehicle_info["upcoming_tls"], tl_schedules, speed_bounds
    )

    if target_speed == -1:
        return
    traci.vehicle.setSpeed(vehicle_info["id"], target_speed)
