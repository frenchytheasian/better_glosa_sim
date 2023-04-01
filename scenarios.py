from pathlib import Path

from networks import generate_network1
from routes import generate_route1

def generate_scenario(name: str, num_intersections: int = 10):
    if not Path('data').exists():
        Path('data').mkdir()
    
    generate_network1(name, num_intersections)
    generate_route1(name)