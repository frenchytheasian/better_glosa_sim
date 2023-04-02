from pathlib import Path

from networks import generate_network1
from routes import generate_route1
from additional import generate_tllogic1

def generate_scenario(name: str, num_intersections: int = 10, scenario: int = 1):
    if not Path('data').exists():
        Path('data').mkdir()

    networks = [generate_network1]
    routes = [generate_route1]
    additional = [generate_tllogic1]
    
    networks[scenario - 1](name, num_intersections)
    routes[scenario - 1](name)
    additional[scenario - 1](name)