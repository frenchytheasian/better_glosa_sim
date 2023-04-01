import os
import sys
import optparse

import traci
from sumolib import checkBinary

from scenarios import generate_scenario

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def run():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
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
    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary("sumo")
    else:
        sumoBinary = checkBinary("sumo-gui")

    name = 'test'
    generate_scenario(name)
    traci.start(
        [sumoBinary, "-c", f"data/{name}.sumocfg", "--tripinfo-output", "tripinfo.xml"],
    )
    run()
    
