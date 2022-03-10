from django.test import TestCase, Client
from ..models import EV, ChargeProfile





class TestSimulatorAPIModels(TestCase):
    def test_EV_model_string(self):
        make = EV.objects.create(make="Tesla", model="X", year=2015)
        self.assertEqual(str(make), "Tesla")

    def test_charge_profile_string(self):
        ev = EV.objects.create(make="Tesla", model="X", year=2015)
        coordinate = ChargeProfile.objects.create(x=1, y=1, ev_id=ev)
        self.assertEqual(str(coordinate), "1, 1")
