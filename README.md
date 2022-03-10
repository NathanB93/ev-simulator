# ev-simulator

## Overview

This fullstack web application (Django, MySQL, React) as well as an 8000 word write up were completed during my MSc Software Development Dissertation at the University of Strathclyde (2021). 

Due to increased uptake of electric vehicles (EV), current research predicts unscheduled residential charging poses a threat to the UK's low-voltage distribution network. 

The app is an MVP of a lightweight tool designed to give power grid engineers a fast and efficient way to run preliminary simulations of stochastic EV charging, before investing in more resource intensive simulations.    

## Installation

Once you have cloned the reposito
ry, navigate to the working directory using the below command:  

`cd EVChargingSimulator`  

To set a database for the application open the settings.py file within EVChargingSimulator find the below code and update the below code to your chosen database:  

```
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'yourdatabase',  
        'USER': 'exampleuser',  
        'PASSWORD': 'exampledatabase',  
        'HOST': 'localhost',  
        'PORT': '3306'  
    }  
}  
```  

Next, install front end dependencies by navigating to the 'front-end` folder using the below command:  

`cd front-end\front-end`  

Once there, execute: 

`npm install`

Once dependencies are installed, execute the build script using:  

`npm run build`  


Now, navigate up two directories to EVChargingSimulator and run the application by executing:  

`python manage.py runserver`  

Then open another terminal and execute to open the interactive python shell using:  

`python manage.py shell`  

For demonstration purposes the program includes the `populateDatabase()` function, which when called populates the database with some example data to quickly explore functionality.   

Enter the following code in the shell:   

```
from SimulatorAPI.utilities import populate_database  

populateDatabase()   
```

The program processes queued simulations asynchronously using `django_background_tasks` as such, a chron job must be initiated on booting up the application server by executing the below code in the shell:  

``` 
from SimulatorAPI.tasks import simulate_scenario     

simulate_scenario(repeat=1, repeat_until=None)  

```

Finally open a new terminal navigate to working directory and execute:  

`python manage.py process_tasks`   
 
The application should now be fully operational and you can begin to run your own simulations!!!  

## Features 

This project includes:
  
    Ability to select a grid network to simulate
  
    Ability to assign different EVs to houses on a selected network
  
    Ability to set a maximum current thersehold for grid cabling
  
    Ability to run a simulation of current demand of stochastic EV charging 
  
    Ability to view the results on a current time plot, and inspect whether the maximum current  
    threshold was exceeded 

## Technologies

    
  Django==3.2.4  
  
  djangorestframework==3.12.4  
  
  django-background-tasks==1.2.5  
  
  django-cors-headers==3.7.0  
  
  mysqlclient==2.0.3  
  
  numpy  
  
  scipy==1.7.0  
  
  Sphinx==4.1.2  
 
  bootstrap: 3.4.1  
  
  react-bootstrap: 1.6.1
  
  chart.js: 3.5.0
  
  react-chartjs-2: 3.0.4
  
  react: 17.0.2  
  
  react-dom: 17.0.2
  
  react-scripts: 4.0.3
  
  Babel==2.9.1
  
  web-vitals: 1.1.2  




