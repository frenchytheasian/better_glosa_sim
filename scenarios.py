from pathlib import Path

from networks import generate_network1
from routes import generate_route1

def generate_sumocfg(name: str):
    with open(f'data/{name}.sumocfg', 'w') as f:
        f.write(
f"""<?xml version="1.0" encoding="UTF-8"?>

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">

    <input>
        <net-file value="{name}.net.xml"/>
        <route-files value="{name}.rou.xml"/>
    </input>

    <time>
        <begin value="0"/>
    </time>

    <report>
        <verbose value="true"/>
        <no-step-log value="true"/>
    </report>

</configuration>
""")

def generate_scenario(name: str):
    if not Path('data').exists():
        Path('data').mkdir()
    
    generate_network1(name)
    generate_route1(name)
    generate_sumocfg(name)

if __name__ == "__main__":
    generate_scenario('test')