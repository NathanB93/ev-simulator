from django.test import TestCase, Client
from unittest import mock
from ..simulation import *
from ..models import Scenario

# Create your tests here.
class URLTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ScenarioDataTests(TestCase):
    def setUp(self):
        @mock.patch("Scenario")
        def mock_scenario(mock_class):
            mock_scenario = create_autospec(Scenario)




class NetworkControllerTests(TestCase):
    def setUp(self) -> None:
        self.mock = Mock()


class HouseControllerTests(TestCase):
    pass


class EVControllerTests(TestCase):
    pass


class ScenarioTests(TestCase):
    pass
