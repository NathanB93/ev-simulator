from rest_framework import serializers
from .models import EV, Scenario, NetworkConfiguration, Node, House, ChargeProfile, HouseEVs, SolarPanel \
    , Connections, Job, Result, BackgroundCurrent, DriverBehaviour


class EVSerializer(serializers.ModelSerializer):
    class Meta:
        model = EV
        fields = ['ev_id', 'make', 'model', 'year', 'battery_charge']


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['house_id', 'name', 'node_id', 'EVs']


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['node_id', 'name', 'network_id', 'connections']


class NetworkConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkConfiguration
        fields = ['network_id', 'name', 'substation']


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['scenario_id', 'name', 'cable_spec', 'network_id']


class ChargeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeProfile
        fields = ['charge_profile_id', 'x', 'y', 'ev_id']


class HouseEVsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseEVs
        fields = ['house_ev_id', 'scenario', 'house', 'ev']


class SolarPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarPanel
        fields = ['solar_panel_id', 'name']


class ConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connections
        fields = ['node', 'connection_id']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_id', 'scenario', 'status']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['result_id', 'total_charge_x', 'total_charge_y', 'scenario_id']


class DriverBehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverBehaviour
        fields = ['hour', 'arrival_probability']


class BackgroundCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundCurrent
        fields = ['hour', 'background_current']
