from django.contrib import admin
from .models import EV, Scenario, NetworkConfiguration, Node, House, ChargeProfile, HouseEVs, SolarPanel \
    , Connections, Job, Result, DriverBehaviour, BackgroundCurrent
# Register your models here.

admin.site.register(EV)
admin.site.register(House)
admin.site.register(Scenario)
admin.site.register(NetworkConfiguration)
admin.site.register(Node)
admin.site.register(ChargeProfile)
admin.site.register(HouseEVs)
admin.site.register(SolarPanel)
admin.site.register(Connections)
admin.site.register(Job)
admin.site.register(Result)
admin.site.register(DriverBehaviour)
admin.site.register(BackgroundCurrent)