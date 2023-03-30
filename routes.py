import random

def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1.0 / 10
    pEW = 1.0 / 11
    pNS = 1.0 / 30
    with open("data/cross.rou.xml", "w") as routes:
        print(
            """<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />""",
            file=routes,
        )
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print(
                    '    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />'
                    % (vehNr, i),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print(
                    '    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />'
                    % (vehNr, i),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print(
                    '    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>'
                    % (vehNr, i),
                    file=routes,
                )
                vehNr += 1
        print("</routes>", file=routes)
