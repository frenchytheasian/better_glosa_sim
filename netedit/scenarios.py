from pathlib import Path

from netedit.networks import generate_network1
from netedit.routes import generate_route1
from netedit.additional import generate_tllogic1

def generate_scenario():
    """
    Generate a scenario with a given number of intersections
    """
    if not Path('data').exists():
        Path('data').mkdir()
    
    generate_network1()
    generate_route1()
    generate_tllogic1()