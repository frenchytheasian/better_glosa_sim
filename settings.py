import optparse


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option(
        "--nogui",
        action="store_true",
        default=False,
        help="run the commandline version of sumo",
    )
    optParser.add_option(
        "--intersections",
        action="store",
        default=10,
        help="set number of intersections",
    )
    optParser.add_option(
        "--filename", action="store", default="test", help="set filename"
    )
    optParser.add_option("--seed", action="store", default=0, help="set seed")
    optParser.add_option("--pcc", action="store_true", default=False, help="use pcc")
    options, args = optParser.parse_args()

    return options
