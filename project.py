"""
This script runs the project with the necessary configurations to generate the needed
output for my project.
"""
import subprocess

from output.parse_xml import get_runtime


def main():
    # TODO output the totals from the analysis
    seed = "1"

    # Run with pcc
    subprocess.run(["python", "runner.py", "--pcc", "--nogui", "--seed", seed])
    subprocess.run(["python", "graph.py", "-a", "speed"])
    subprocess.run(["python", "graph.py", "-a", "CO2"])

    with open("output/runtime.txt", "w") as f:
        f.write(str(get_runtime()) + "\n")

    # Run without pcc
    subprocess.run(["python", "runner.py", "--nogui", "--seed", seed])
    subprocess.run(["python", "graph.py", "-a", "speed"])
    subprocess.run(["python", "graph.py", "-a", "CO2"])

    with open("output/runtime.txt", "a") as f:
        f.write(str(get_runtime()) + "\n")


if __name__ == "__main__":
    main()
