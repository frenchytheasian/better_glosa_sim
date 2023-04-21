import os
import sys

import traci
from sumolib import checkBinary

from netedit.scenarios import generate_scenario
from pcc.getters import get_static_signal_schedule, get_state
from pcc.setters import adjust_speed
from output.visualize import visualize
from settings import get_options

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def run(name: str):
    """
    execute the TraCI control loop

    Args:
        name (str): name of the scenario
    """
    step = 0
    tl_schedules = get_static_signal_schedule(name)
    # we start with phase 2 where EW has green
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        state = get_state()

        for vehicle in state.keys():
            adjust_speed(state[vehicle], tl_schedules)
        
        step += 1
    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary("sumo")
    else:
        sumoBinary = checkBinary("sumo-gui")

    name = options.filename
    generate_scenario()

    traci.start(
        [sumoBinary, "-n", f"data/{name}.net.xml", "-r", f"data/{name}.rou.xml", "-a", f"data/{name}.add.xml", "--tripinfo-output", "output/tripinfo.xml", "--emission-output", "output/emission.xml", "--full-output", "output/full.xml"],
    )
    run(name)

    speed = visualize("speed")
    c02 = visualize("CO2")

    print(f"Average speed: {speed}")
    print(f"Total CO2: {c02}")
    os.system(f"rm -rf data")