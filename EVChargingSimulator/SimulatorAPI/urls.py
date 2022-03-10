from django.urls import path, include

from .views import NetworkConfigDropdown, EVDropdown, NodeAPIView, ScenarioAPIView, HouseEVsAPIView, JobAPIView, \
    HouseAPIView, ResultAPIView

urlpatterns = [

    path('network-list/', NetworkConfigDropdown.as_view()),
    path('ev-list/', EVDropdown.as_view()),
    path('nodes/<int:network>/', NodeAPIView.as_view()),
    path('houseevs/', HouseEVsAPIView.as_view()),
    path('houseevs/<int:pk>/', HouseEVsAPIView.as_view()),
    path('scenario/', ScenarioAPIView.as_view()),
    path('scenario/<int:pk>/', ScenarioAPIView.as_view()),
    path('job/', JobAPIView.as_view()),
    path('job/<int:pk>/', JobAPIView.as_view()),
    path('house/<int:node>/', HouseAPIView.as_view()),
    path('results/<int:scenario>/', ResultAPIView.as_view())

]



