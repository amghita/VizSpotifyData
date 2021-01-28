# Spotify Data Vizualization with Apache Airflow


Data Visualization is one of the essential aspects of Data Science. It can either be used for data exploration or communicate the result of the analysis. During data exploration, visualization can reveal hidden information in our data. 

## What is Airflow and how can it help ?
Apache Airflow is a workflow management platform that allows users to programmatically schedule jobs that run on a standalone basis and to monitor them through its user interface. Airflow’s main components are a Webserver (Airflow’s UI build as a Flask App), a Scheduler, an Executor and a Metadata Database.


This is a short tutorial to show how I combined Python and Airflow to create an automated Pipeline to visualize Spotify song Data. We have 2 main files :
1. pipeline_spotify.py
2. dashboard.py

## Set up 

### Install and configure Airflow 

1. Activate your virtual environment , and run pip intsall apache-airflow 
2. Call the airflow initdb command to initiate the SQLite database where Airflow will store the metadata that are necessary to manage your workflow.
3. 

You can follow the quick start guid from apache airflow http://airflow.apache.org/docs/apache-airflow/stable/start.html
## Visualisation and Dashboard







## Ressources 

1. Airflow 
2. Guide Spotify API
3. Plotly 
4. Flask 
