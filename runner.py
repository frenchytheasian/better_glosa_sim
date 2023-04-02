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
    optParser.add_option(
        "--scenario",
        action="store",
        default=1,
        help="set scenario"
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
    generate_scenario(name, int(options.intersections), int(options.scenario))
    traci.start(
        [sumoBinary, "-n", f"data/{name}.net.xml", "-r", f"data/{name}.rou.xml", "-a", f"data/{name}.add.xml", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emission.xml"],
    )
    run()
    os.system(f"rm -rf data")