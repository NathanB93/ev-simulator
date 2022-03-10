import csv

from .models import ChargeProfile, EV, BackgroundCurrent, DriverBehaviour, NetworkConfiguration, Node, House


def charge_profile_reader(file_name: str, ev: EV):
    """ Function to upload a csv of an EVs charging profile to the database

    Args:
        file_name: the path of csv file
        ev: the EV the charge profile belongs to
    """

    with open(file_name, newline='') as charge_profile:
        reader = csv.reader(charge_profile)
        next(reader)

        for row in reader:
            entry = ChargeProfile(x=row[0], y=row[1], ev_id=ev)
            entry.save()

    charge_profile.close()


def background_current_loader(file_name: str):
    """Function to upload a csv file containing background current data to the database

    Args:
        file_name: the path of csv file

    """
    x = []
    y = []
    with open(file_name, newline='') as background_profile:
        reader = csv.reader(background_profile)
        next(reader)
        hour = 0
        for row in reader:
            current = float(row[1]) / 230.0
            entry = BackgroundCurrent(hour=hour, background_current=current)
            entry.save()
            hour += 1

    background_profile.close()


def driver_behaviour_loader(file_name: str):
    """Function to upload a csv of an background current data to the database

    Args:
        file_name: the path of csv file

    """
    x = []
    y = []
    with open(file_name, newline='') as background_profile:
        reader = csv.reader(background_profile)
        next(reader)
        hour = 0
        for row in reader:
            freq = float(row[1])
            entry = DriverBehaviour(hour=hour, arrival_probability=freq)
            entry.save()
            hour += 1

    background_profile.close()


def populate_database():

    nc1 = NetworkConfiguration(name="Network_1")
    nc1.save()

    node_sub1 = Node(name="Substation_1")
    node_sub1.save()

    node_house1 = Node(name="House_1")
    node_house1.save()

    house1 = House(node_id=node_house1)
    house1.save()

    node_house2 = Node(name="House_2")
    node_house2.save()

    house2 = House(node_id=node_house2)
    house2.save()

    node_house3 = Node(name="House_3")
    node_house3.save()

    house3 = House(node_id=node_house3)
    house3.save()

    node_house4 = Node(name="House_4")
    node_house4.save()

    house4 = House(node_id=node_house4)
    house4.save()

    node_house5 = Node(name="House_5")
    node_house5.save()

    house5 = House(node_id=node_house5)
    house5.save()

    nc2 = NetworkConfiguration(name="Network_2")
    nc2.save()

    node_sub2 = Node(name="Substation_2")
    node_sub2.save()

    node_house6 = Node(name="House_6")
    node_house6.save()

    house6 = House(node_id=node_house6)
    house6.save()

    node_house7 = Node(name="House_7")
    node_house7.save()

    house7 = House(node_id=node_house7)
    house7.save()

    node_house8 = Node(name="House_8")
    node_house8.save()

    house8 = House(node_id=node_house8)
    house8.save()

    ev1 = EV(make="BMW", model="i3", year=2020)
    ev1.save()

    ev2 = EV(make="Tesla", model="x", year=2020)
    ev2.save()

    charge_profile_reader('Data/ChargingCurveFinal.csv', ev1)
    charge_profile_reader('Data/ChargingCurveFinal.csv', ev2)


def initialise_data():
    background_current_loader('Data/backgroundCurrent.csv')
    driver_behaviour_loader('Data/DriverBehaviour.csv')
