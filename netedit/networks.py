import subprocess
from settings import get_options


def generate_nod1():
    """
    Generates a .nod.xml file for a network with a given number of intersections
    """
    options = get_options()
    name = options.filename
    num_intersections = int(options.intersections)
    temp_nod_file = open("data/nod.tmp", "a")

    with open(f"data/{name}.nod.xml", "w") as f:
        f.write(
            f"""<?xml version="1.0" encoding="UTF-8"?>
<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">
    <node id="beg" x="-1000" y="0" type="priority" />
    <node id="end" x="{num_intersections * 1000}" y="0" type="priority" />

"""
        )

        for i in range(0, num_intersections):
            f.write(
                f"""\t<node id="{i}" x="{i*1000}" y="0" type="traffic_light" />\n"""
            )
            temp_nod_file.write(f"{i} ")

        f.write("""</nodes>""")
    temp_nod_file.close()


def generate_edg1():
    """
    Generates a .edg.xml file for a network with a given number of intersections
    """
    options = get_options()
    name = options.filename
    num_intersections = int(options.intersections)
    edges = []
    with open(f"data/{name}.edg.xml", "w") as f:
        f.write(
            """<?xml version="1.0" encoding="UTF-8"?>
<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">

"""
        )
        f.write(
            """\t<edge \
                id="0r" from="beg" to="0" numLanes="1" \
                priority="78" speed="20.11" />\n \
            """
        )
        edges.append("0r")
        for i in range(1, num_intersections):
            f.write(
                f"""\t<edge \
                    id="{i}r" from="{i-1}" to="{i}" \
                    numLanes="1" priority="78" speed="20.11" />\n \
                """
            )
            edges.append(f"{i}r")

        f.write(
            f"""\t<edge id="{num_intersections}r" from="{num_intersections - 1}" \
                to="end" numLanes="1" priority="78" speed="20.11" />\n \
            """
        )
        edges.append(f"{num_intersections}r")

        f.write("""</edges>""")

    with open("data/edges.tmp", "w") as f:
        f.write(",".join(edges))


def generate_network1():
    """Generate a network with a given number of intersections"""
    options = get_options()
    name = options.filename

    generate_nod1()
    generate_edg1()
    subprocess.run(
        [
            "netconvert",
            "-n",
            f"data/{name}.nod.xml",
            "-e",
            f"data/{name}.edg.xml",
            "-o",
            f"data/{name}.net.xml",
        ]
    )
