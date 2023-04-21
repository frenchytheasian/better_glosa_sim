from optparse import OptionParser

from output.visualize import visualize


def get_options():
    parser = OptionParser()

    # Valid options: CO2, CO, HC, NOx, PMx, fuel, electricity, noise, waiting, pos,
    # speed, x, y
    parser.add_option(
        "-a", "--attrib", action="store", default="speed", help="attribute to visualize"
    )

    options, args = parser.parse_args()

    return options


if __name__ == "__main__":
    options = get_options()
    visualize(options.attrib)
