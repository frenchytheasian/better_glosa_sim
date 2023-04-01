import subprocess

def generate_nod1(name: str):
    with open(f'data/{name}.nod.xml', 'w') as f:
        f.write(
f"""<?xml version="1.0" encoding="UTF-8"?>
<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">
    <node id="beg" x="0" y="0" type="priority" />
    <node id="end" x="1000" y="0" type="priority" />

""")
        for i in range(1, 10):
            f.write(f"""\t<node id="{i}" x="{i*100}" y="0" type="traffic_light" />\n""")

        f.write("""</nodes>""")
                
def generate_edg1(name: str):
    with open(f'data/{name}.edg.xml', 'w') as f:
        f.write(
f"""<?xml version="1.0" encoding="UTF-8"?>
<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">

""")
        f.write(f"""\t<edge id="1r" from="beg" to="1" numLanes="1" priority="78" speed="13.89" />\n""")
        for i in range(2, 10):
            f.write(f"""\t<edge id="{i}r" from="{i-1}" to="{i}" numLanes="1" priority="78" speed="13.89" />\n""")
        f.write(f"""\t<edge id="10r" from="9" to="end" numLanes="1" priority="78" speed="13.89" />\n""")

        f.write("""</edges>""")

def generate_network1(name: str):
    generate_nod1(name)
    generate_edg1(name)
    subprocess.run(['netconvert', '-n', f'data/{name}.nod.xml', '-e', f'data/{name}.edg.xml', '-o', f'data/{name}.net.xml'])