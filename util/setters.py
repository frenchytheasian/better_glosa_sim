from typing import List, Tuple, Dict

import traci

####################
### Adjust Speed ###
####################
def _get_speed_bounds(vehicle_info: dict) -> Tuple[float, float]:
    """get the speed bounds of the vehicle
    
    This is currently a simplified version of the speed bounds."""
    min_v = 1.0
    max_v = traci.vehicle.getAllowedSpeed(vehicle_info['id'])
    return min_v, max_v

def _get_v_bound_for_tl(tl: Dict[str, int], tl_schedules: dict, env_v_bound: Tuple[int, int]) -> Tuple[float, float]:
    time = traci.simulation.getTime()
    id, distance = tl.popitem()
    tl_schedule = [x - time for x in tl_schedules[id]]
    
    for i in range(0, len(tl_schedule), 2):
        if tl_schedule[i + 1] <= 0:
            continue

        v_low = distance / tl_schedule[i + 1]
        if tl_schedule[i] <= 0:
            v_high = float('inf')
        else:
            v_high = distance / tl_schedule[i]
        
        if not v_low <= env_v_bound[1] and v_high >= env_v_bound[0]:
            continue
        else:
            return max(v_low, env_v_bound[0]), min(v_high, env_v_bound[1])


def _get_target_speed(upcoming_tls: List[dict], tl_schedules: dict, env_v_bound: Tuple[float, float]) -> float:
    """get the target speed of the vehicle"""
    valid_bounds = {}
    for tl in upcoming_tls:
        key = list(tl.keys())[0]
        valid_bound = _get_v_bound_for_tl(tl, tl_schedules, env_v_bound)
        valid_bounds[key] = valid_bound
    
    
def adjust_speed(vehicle_info: dict, tl_schedules: dict):
    speed_bounds = _get_speed_bounds(vehicle_info)
    target_speed = _get_target_speed(vehicle_info['upcoming_tls'], tl_schedules, speed_bounds)