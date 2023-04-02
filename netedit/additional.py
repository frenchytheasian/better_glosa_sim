import random
import os

def generate_tllogic1(name: str):
    red_duration = [10, 30]
    green_duration = [10, 30]

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
            f.write(f"""\n\t</tlLogic>""")

        f.write(f"""</additional>""")

        