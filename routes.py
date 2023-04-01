import random

def generate_route1(name: str):
    N = 1000
    demand = 1.0 / 10

    with open(f'data/{name}.rou.xml', 'w') as f:
        f.write(
f"""<routes>
    <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
    <route id="right" edges="1r 2r 3r 4r 5r 6r 7r 8r 9r 10r" />
""")

        for i in range(N):
            if random.uniform(0, 1) < demand:
                f.write(
                    f'\t<vehicle id="right_{i}" type="type1" route="right" depart="{i}" />\n'
                )
        
        f.write("</routes>")