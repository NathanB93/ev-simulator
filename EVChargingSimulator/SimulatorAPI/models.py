from django.db import models


# Create your models here.

class EV(models.Model):
    """

    Stores a single electric vehicle (EV)

    """
    ev_id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    battery_charge = 100

    def get_profile(self):
        times = self.profile.all().values_list('x', flat =True)
        time_list = [time for time in times]
        currents = self.profile.values_list('y', flat=True)
        current_list = [current for current in currents]
        return time_list, current_list

    def __str__(self):
        return self.make


class ChargeProfile(models.Model):
    """
    Stores a single point on the charge profile of an EV, related to :model: 'SimulatorAPI.EV'
    """
    charge_profile_id = models.AutoField(primary_key=True)
    x = models.FloatField(default=1)
    y = models.FloatField(default=1)
    ev_id = models.ForeignKey(EV, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return str(self.x) + ", " + str(self.y)


class NetworkConfiguration(models.Model):

    """
    Stores a single network configuration, related to: model: 'SimulatorAPI.Node'
    """
    network_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    substation = models.ForeignKey('Node', on_delete=models.CASCADE, null=True, blank=True)

    def get_nodes(self):

        nodes = list(self.node_set.all())
        return nodes

    def __str__(self):
        return self.name


class Node(models.Model):
    """
    Stores a single node entry, which represents either a house or a substation on a
    network, model: related to :model:'SimulatorAPI.NetworkConfiguration' and :model:'SimulatorAPI.Connections

    """
    node_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    network_id = models.ForeignKey('NetworkConfiguration', on_delete=models.CASCADE, default=1)
    connections = models.ManyToManyField("self", through='Connections', blank=True)

    def __str__(self):
        return self.name


class House(models.Model):
    """

    Stores a single house, related to :model: 'SimulatorAPI.Node' and :model: 'SimulatorAPI.EV'

    """

    # TODO remove name field
    house_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    current = models.IntegerField(null= True, blank=True)
    EVs = models.ManyToManyField(EV, through='HouseEVs', related_name='evs')


class SolarPanel(models.Model):
    # TODO either incorporate or remove
    solar_panel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class Scenario(models.Model):

    """

    Stores a single scenario, related to :model:'SimulatorAPI.NetworkConfiguration'.

    """
    scenario_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    cable_spec = models.IntegerField()
    network_id = models.ForeignKey(NetworkConfiguration, on_delete=models.CASCADE)

    def get_house_evs(self):
        house_evs = list(self.houseevs_set.all())
        return house_evs

    def __str__(self):
        return self.name


class HouseEVs(models.Model):

    house_ev_id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    ev = models.ForeignKey(EV, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)


class Connections(models.Model):
    """

    Stores a single connection between nodes, related to :model: 'SimulatorAPI.Node'

    """
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node')
    connection_id = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='connection')


class Job(models.Model):

    """

    Stores a single job, related to :model: 'SimulatorAPI.Scenario'

    """
    job_id = models.AutoField(primary_key=True)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)


class Result(models.Model):

    """

    Stores a single current/time plot entry from a simulated scenarios results.
    Related to :model: 'SimulatorAPI.Scenario'

    """
    result_id = models.AutoField(primary_key=True)
    total_charge_x = models.IntegerField()
    total_charge_y = models.FloatField()
    scenario_id = models.ForeignKey(Scenario, on_delete=models.CASCADE)


class DriverBehaviour(models.Model):
    """

    Stores a single bin and bin entry for a driver behaviour histogram

    """
    # TODO change field names
    hour = models.IntegerField(primary_key=True)
    arrival_probability = models.FloatField()


class BackgroundCurrent(models.Model):
    """

    Stores a single bin and bin entry for a background current histogram

    """
    hour = models.IntegerField(primary_key=True)
    background_current = models.FloatField()

    def get_background_current(self):
        currents = self.objects.all().values_list('hour', 'background_current')
        current_list = [current for current in currents]
        return current_list



