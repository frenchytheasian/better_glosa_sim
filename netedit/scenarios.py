from pathlib import Path

from netedit.networks import generate_network1
from netedit.routes import generate_route1
from netedit.additional import generate_tllogic1

def generate_scenario(name: str, num_intersections: int = 10):
    """
    Generate a scenario with a given number of intersections

    Args:
        name (str): name of the network
        num_intersections (int, optional): number of intersections. Defaults to 10.
    """
    if not Path('data').exists():
        Path('data').mkdir()
    
    generate_network1(name, num_intersections)
    generate_route1(name)
    generate_tllogic1(name)