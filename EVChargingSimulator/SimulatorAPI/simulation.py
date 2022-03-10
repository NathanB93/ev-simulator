import numpy as np
import scipy.stats
import random
from .models import Result, DriverBehaviour, BackgroundCurrent, House, EV, Scenario, Node


class ScenarioData:
    """ A class to retrieve and manipulate a given Scenarios data in order for it to be simulated, as
    well as post the results to the database.

    Attributes:

        scenario: the Scenario to handle data for
        house_ev_dict : a dictionary mapping EVs to Houses
        house_ev_dict : dict
        charge_profile_dict : a dictionary holding each EVs charge profile
        charge_profile_dict : dict

    """

    def __init__(self, scenario: Scenario):
        """Constructor method for ScenarioData class """
        self.scenario = scenario
        self.house_ev_dict = {}
        self.charge_profile_dict = {}

    def network(self):
        """ Returns the network associated with the Scenario

        Returns: the Scenarios network
        """
        network = self.scenario.network_id
        return network

    def get_substation(self):
        """ Returns the Scenarios substation

        Returns: the Scenarios substation
        """
        substation = self.network().substation
        return substation

    def nodes(self):
        """ Returns all nodes on the Scenarios Network

        Returns: a list of node objects on the Scenarios Network
        """
        network = self.scenario.network_id
        nodes = network.get_nodes()
        return nodes

    def background_current(self):
        """ Populates a list with average Background Current values

         Returns: a list of background current values for each hour of the day
         """
        currents = BackgroundCurrent.objects.all().values_list('background_current', flat=True)
        current_list = [current for current in currents]
        return current_list

    def driver_behaviour(self):
        """ A method to load driver charging behaviour data required for determining arrival times

        Returns: a tuple containing a numpy array of the bins/frequencies of EV charging events
                over a 24 hour period
        """

        # change hour to floatfield in model!!!!!!!
        bins = DriverBehaviour.objects.all().values_list('hour', flat=True)
        bins_lst = [float(bin) for bin in bins]
        bins_lst.append(24.0)

        arrival_freqs = DriverBehaviour.objects.all().values_list('arrival_probability', flat=True)
        arrival_freqs = [freq for freq in arrival_freqs]

        return np.array(arrival_freqs), np.array(bins_lst)

    def houses(self):
        """ A method to return all the Houses on the Scenarios Network



        Returns: a list of all Houses on the Scenario's Network
        """
        houses = []
        substation = self.get_substation()
        nodes = self.nodes()

        for node in nodes:
            if node == substation:
                continue
            else:
                house = House.objects.get(node_id=node)
                houses.append(house)
        return houses

    def charge_profiles(self):
        """ A method to retrieve and set the charge profiles for all EVs associated with Scenario

        Retrieves charge profiles from the database and populates a dictionary with EVs as keys and their
        charge profiles as values
        """
        for house in self.house_ev_dict:
            for ev in self.house_ev_dict[house]:
                if ev.ev_id not in self.house_ev_dict:
                    self.charge_profile_dict[ev] = ev.get_profile()

    # could be named better!!!!!
    def assign_evs(self):
        """ A method to assign EVs to Houses on the Scenarios Network

        Populates house_ev_dict mapping EVs to their assigned houses for use by the
        House Controller class
        """
        house_ev_list = self.scenario.get_house_evs()

        for relation in house_ev_list:

            if relation.house in self.house_ev_dict:
                self.house_ev_dict[relation.house].append(relation.ev)
                continue

            self.house_ev_dict[relation.house] = [relation.ev]

    def post_results(self, current_profile: list):
        """ A method to post the results of a simulation to the Results DB table

        Args:
            current_profile : a list of current values outputted by thr Simulation of a Scenario

        """

        for i in range(len(current_profile)):
            result = Result(total_charge_x=i, total_charge_y=current_profile[i], scenario_id=self.scenario)
            result.save()


class NetworkController:
    """ A class to manage a Scenarios Network and determine the total current demand throughout a Simulation

    Attributes

        substation: the Node object that is the Networks Substation
        houses: a list of all the houses on the Network
        house_controller: the HouseController for the Simulation

    """

    def __init__(self, substation: 'Node', houses: list, house_controller: 'HouseController'):
        """Constructor method for Network Controller Class
                """
        self.substation = substation
        self.houses = houses
        self.hc = house_controller

    def substation_current(self, minute):
        """ A method to determine the current demand on a substation at a given minute

        Calculates the cumulative total of all components charge demand on the
        substation at a given minute

        Args:
            minute: the minute count of the simulation being run

        Return: the total current demand on the Networks Substation at a given minute
        """
        substation_current = 0
        for house in self.houses:
            substation_current += self.hc.house_current(house, minute)
        return substation_current


class HouseController:
    """ A class to simulate events and processes associated with a Scenarios Houses

    Args:
        ev_controller: the EV Controller for the associated Simulation
        house_evs: a dictionary containing the Scenarios EVs assigned to their Houses
        bc: a list of background current values for each hour of the day
    """

    def __init__(self, ev_controller: 'EVController', bc: list, house_evs: dict):
        """ Constructor method for HouseController Class"""

        self.ev_controller = ev_controller
        self.house_ev_dict = house_evs
        self.background_current = bc
        self.arrivals_dict = {}

    def house_current(self, house: 'House', minute: int):
        """ A method to calculate the total current demand of a house at a given time

        Calculates the total current demand of a house at a given minute, by adding background current
        to the sum of any EVs charging current at that minute.

        Args:
            house: the House object to calculate current for
            minute: the minute count of the simulation being run

        Returns: the total current(A) demand on the Networks Substation at a given minute
            Returned: int
        """

        background_current = self.background_current[int(minute / 60)]
        charging_current = 0

        if house in self.house_ev_dict:
            for index, ev in enumerate(self.house_ev_dict[house]):
                arrival_time = self.arrivals_dict[house][index]
                charging_current += self.ev_controller.ev_current(ev, arrival_time, minute)

            total_current = background_current + charging_current
            return total_current
        return background_current

    def schedule_arrivals(self, es: 'EventScheduler'):
        """ A method to schedule the arrival times of all EVs associated with a Scenario

        Populates the arrivals_dict dictionary mapping Houses to a list of arrival times

        Attributes:

            es: EventScheduler for the associated simulation


        """
        for house in self.house_ev_dict:
            for i in range(len(self.house_ev_dict[house])):
                arrival_time = es.generate_arrival_time()
                if house in self.arrivals_dict:
                    self.arrivals_dict[house].append(arrival_time)
                    continue
                self.arrivals_dict[house] = [arrival_time]


class EVController:
    """ A class to simulate processes associated with the associated scenarios EVs

    The EVController class determines the current drawn by the residential charging of EVs

    Attributes:
        charge_profiles: a dictionary mapping EVs to their charging profiles
    """

    def __init__(self, charge_profiles: dict):
        """Constructor method for EVControllerClass"""

        self.charge_profile_dict = charge_profiles

    def ev_current(self, ev: EV, arrival_time: int, minute: int):
        """ A method to return the charging current demand of an EV at a given time, determined from
        the EVs charge profile


        Args:
            minute: the minute count from Simulation class
            arrival_time: the EVs scheduled arrival time
            ev: The EV object to determine the current demand from

        Return: the current drawn by the given EV at the given minute
        """
        if arrival_time <= minute < arrival_time + len(self.charge_profile_dict[ev][0]):
            power = self.charge_profile_dict[ev][1][minute - arrival_time]
            current = (power * 1000) / 230
            return current
        current = 0
        return current


class EventScheduler:
    """A class to randomly determine EV arrival time in accordance with driver behaviour data


    Class to represent a simulation, allows the running of Simulation, as well as the recording
     , manipulation and saving of results.

    Attributes:
        hist: a tuple containing two numpy arrays, representing the bins and frequencies of a histogram

    """

    def __init__(self, hist: tuple):
        """ constructor for the EventScheduler class """
        self.hist = hist
        self.hist_dist = []
        self.sim_time = []

    def distribution(self):
        """A method to create a distribution curve from histogram data"""
        # Create a distribution from the histogram, using linear interpolation.
        self.hist_dist = scipy.stats.rv_histogram(self.hist)

    def generate_arrival_time(self):
        """ A method to generate an EVs arrival time

        Returns: an arrival time for an EV
            Returned: int
        """
        q = random.uniform(0, 1)
        arrival_time = self.hist_dist.ppf(q)
        arrival_time_mins = int(arrival_time * 60.0)
        return arrival_time_mins


class Simulation:
    """

    Class to represent a simulation, allows the running of Simulation, as well as the recording
     ,manipulation and saving of results.

    Attributes:
        nc: The Simulations NetworkController
        hc: The Simulations HouseController
        es: The Simulations EventScheduler
        current_profile: a list to hold the current profile data created by run_simulation()
    """

    def __init__(self, nc: NetworkController, hc: HouseController, es: EventScheduler):
        self.nc = nc
        self.hc = hc
        self.es = es
        self.current_profile = []

    def run_simulation(self, days):
        """ Starts running a simulation for a given number of days, and logs the current profile in current_profile

        Args:
            days: the number of days the simulation should run

        """
        for day in range(days):
            self.hc.schedule_arrivals(self.es)
            daily_current_profile = []
            for minute in range(1440):
                daily_current_profile.append(self.nc.substation_current(minute))
            self.current_profile.append(daily_current_profile)

    def average_profile(self):
        """ Averages the daily current profiles created by run_simulation returning a single averaged profile

        Returns average_profile a list containing the averaged profile
            Returned: list of integer elements, values are the current, and the index corresponds to the minute in the day
        """
        average_profile = []
        for index_i, i in enumerate(self.current_profile):
            for index_j, j in enumerate(i):
                if len(average_profile) < len(i):
                    average_profile.append(j)
                    continue
                elif index_i == (len(self.current_profile) - 1):
                    average_profile[index_j] = (average_profile[index_j] + j) / len(self.current_profile)
                    continue
                average_profile[index_j] += j
        return average_profile

    def return_results(self, sd: ScenarioData):
        """ Passes results to ScenarioData to be posted to db

        Args:
            sd: the ScenarioData class for the Simulation
        """
        profile = self.average_profile()
        sd.post_results(profile)
