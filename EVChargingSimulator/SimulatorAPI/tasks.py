from background_task import background
from .models import Job
from .simulation import Simulation, ScenarioData, EventScheduler, EVController, NetworkController, HouseController


@background()
def simulate_scenario():
    """ A function to schedule the simulation of scenarios queued in the Job db table """

    try:
        job = Job.objects.all().filter(status='waiting')[0]

    except IndexError:
        return print('no simulations queued')

    else:

        job.status = 'running'
        job.save(update_fields=["status"])

        scenario = job.scenario
        sd = ScenarioData(scenario)
        sd.assign_evs()
        sd.charge_profiles()
        hist = sd.driver_behaviour()

        es = EventScheduler(hist)
        es.distribution()

        charge_profiles = sd.charge_profile_dict
        evc = EVController(charge_profiles)

        bc = sd.background_current()

        house_ev_dict = sd.house_ev_dict
        hc = HouseController(evc, bc, house_ev_dict)

        substation = sd.get_substation()
        houses = sd.houses()

        nc = NetworkController(substation, houses, hc)

        sim = Simulation(nc, hc, es)
        sim.run_simulation(1000)

        sim.return_results(sd)

        # updates job status to complete when scenario finished

        job.status = 'complete'
        job.save(update_fields=["status"])
