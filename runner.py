import os
import sys
import optparse

import traci
from sumolib import checkBinary

from netedit.scenarios import generate_scenario
from pcc.getters import get_static_signal_schedule, get_state
from pcc.setters import adjust_speed

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


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option(
        "--nogui",
        action="store_true",
        default=False,
        help="run the commandline version of sumo",
    )
    optParser.add_option(
        "--intersections",
        action="store",
        default=10,
        help="set number of intersections"
    )
    optParser.add_option(
        "--filename",
        action="store",
        default="test",
        help="set filename"
    )
    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary("sumo")
    else:
        sumoBinary = checkBinary("sumo-gui")

    name = options.filename
    generate_scenario(name, int(options.intersections))

    traci.start(
        [sumoBinary, "-n", f"data/{name}.net.xml", "-r", f"data/{name}.rou.xml", "-a", f"data/{name}.add.xml", "--tripinfo-output", "output/tripinfo.xml", "--emission-output", "output/emission.xml", "--full-output", "output/full.xml"],
    )
    run(name)
    os.system(f"rm -rf data")