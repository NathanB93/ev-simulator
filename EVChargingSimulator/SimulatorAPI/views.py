from django.http import Http404
from .serializers import EVSerializer, ScenarioSerializer, NetworkConfigurationSerializer, \
    NodeSerializer, SolarPanelSerializer, HouseSerializer, ChargeProfileSerializer, HouseEVsSerializer \
    , ConnectionsSerializer, JobSerializer, ResultSerializer
from .models import EV, Scenario, SolarPanel, NetworkConfiguration, Node, House, ChargeProfile, HouseEVs \
    , Connections, Job, Result

from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# allows user to create a scenario to be ran
class ScenarioAPIView(APIView):
    def post(self, request):
        serializer = ScenarioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        scenario = Scenario.objects.get(pk=pk)
        scenario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# retrieves and creates relationships between Houses and Cars
class HouseEVsAPIView(APIView):
    def get(self, request, pk):
        relationships = HouseEVs.objects.filter(pk=pk)
        serializer = HouseEVsSerializer(relationships)
        return Response(serializer.data)

    def post(self, request):
        serializer = HouseEVsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        relationship = HouseEVs.objects.get(pk=pk)
        relationship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# gets relevant info for front end network config dropdown
class NetworkConfigDropdown(APIView):

    #needs errors
    def get(self, request):
        config_list = NetworkConfiguration.objects.all()
        serializer = NetworkConfigurationSerializer(config_list, many=True)
        return Response(serializer.data)


class NodeAPIView(APIView):
    # returns all nodes of a given network configuration
    def get(self, request, network):
        nodes = Node.objects.filter(network_id=network)
        serializer = NodeSerializer(nodes, many=True)
        return Response(serializer.data)


# gets relevant information for EV dropdown menu
class EVDropdown(APIView):
    def get(self, request):
        ev_list = EV.objects.all()
        serializer = EVSerializer(ev_list, many=True)
        return Response(serializer.data)


# creates, or retrieves the status of a job for the front end
class JobAPIView(APIView):
    def get_job(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        job = self.get_job(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data['status'])

    def post(self, request):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HouseAPIView(APIView):
    def get_house(self, node):
        try:
            return House.objects.get(node_id=node)
        except House.DoesNotExist:
            raise Http404

    def get(self, request, node):
        house = self.get_house(node)
        serializer = HouseSerializer(house)
        return Response(serializer.data)


# allows retrieval of results
class ResultAPIView(APIView):
    # needs 404 not found exception
    def get_results(self, scenario):
        try:
            return Result.objects.filter(scenario_id=scenario)
        except Result.DoesNotExist:
            raise Http404

    def get(self, request, scenario):
        results = self.get_results(scenario)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
