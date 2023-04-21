import os

from settings import get_options


def generate_route1():
    """
    Generate a random route for the given scenario
    """
    options = get_options()
    name = options.filename

    edges = ""
    with open("data/edges.tmp", "r") as f:
        edges = f.read().split(",")
        edges = " ".join(edges)

    os.remove("data/edges.tmp")

    with open(f"data/{name}.rou.xml", "w") as f:
        f.write(
            f""" \
                <routes>\n \
                \t<vType id="type1" accel="0.8" decel="4.5" sigma="0.5" \
                length="5" minGap="2.5" maxSpeed="55" guiShape="passenger"/>\n \
                \t<route id="right" edges="{edges}" /> \
            """
        )
        v_id = "normal"
        if options.pcc:
            v_id = "pcc"
        f.write(
            f'\t<vehicle id="{v_id}_{0}" type="type1" route="right" depart="{0}" />\n'
        )

        f.write("</routes>")
