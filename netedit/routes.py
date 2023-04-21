import os

from settings import get_options

def generate_route1():
    """
    Generate a random route for the given scenario
    """
    options = get_options()
    name = options.filename
    N = 1000
    demand = 1.0 / 100

    edges = ''
    with open(f'data/edges.tmp', 'r') as f:
        edges = f.read().split(',')
        edges = ' '.join(edges)

    os.remove(f'data/edges.tmp')

    with open(f'data/{name}.rou.xml', 'w') as f:
        f.write(
f"""<routes>
    <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="55" guiShape="passenger"/>
    <route id="right" edges="{edges}" />
""")

        # for i in range(N):
        #     if random.uniform(0, 1) < demand:
        #         f.write(
        #             f'\t<vehicle id="right_{i}" type="type1" route="right" depart="{i}" />\n'
        #         )

        v_id = 'normal'
        if options.pcc:
            v_id = 'pcc'
        f.write(
            f'\t<vehicle id="{v_id}_{0}" type="type1" route="right" depart="{0}" />\n'
        )
        
        f.write("</routes>")