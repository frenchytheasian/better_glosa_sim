import random
import os

from settings import get_options

def generate_tllogic1():
    """
    Generate a random traffic light logic for the given scenario
    """
    name = get_options().filename
    random.seed(42)
    red_duration = [20, 45]
    green_duration = [20, 45]

    edges = []
    with open(f'data/nod.tmp', 'r') as f:
        edges = f.read().strip().split(' ')
    os.remove(f'data/nod.tmp')

    with open(f'data/{name}.add.xml', 'w') as f:
        f.write(f"""<additional>\n""")
        for edge in edges:
            phases = [
                f"""\t\t<phase duration="{random.randrange(*green_duration)}" state="G"/>""",
                f"""\t\t<phase duration="{random.randrange(*red_duration)}" state="r"/>""",
            ]
            random.shuffle(phases)
            f.write(f"""    <tlLogic id="{edge}" type="static" programID="tl{edge}" offset="0">\n""")
            f.write('\n'.join(phases))
            f.write(f"""\n\t</tlLogic>\n""")

        f.write(f"""</additional>""")

        
