# Spotify Data Visualization with Apache Airflow

## Motivation

Data Visualization is one of the essential aspects of Data Science. It can either be used for data exploration or communicate the result of the analysis. During data exploration, visualization can reveal hidden information in our data. 
In effect, while I was building an app to visualize Spotify song Data with Plotly, I realized that every time I wanted data to be updated, I had to re-run the entire code manually. This process takes a very long time when you need to extract, manipulate and make available data for Spotify users.

### What is Airflow and how can it help ?
Apache Airflow is a workflow management platform that allows users to programmatically schedule jobs that run on a standalone basis and to monitor them through its user interface. Airflow’s main components are a Webserver (Airflow’s UI build as a Flask App), a Scheduler, an Executor and a Metadata Database.


This is a short tutorial to show how I combined Python and Airflow to create an automated Pipeline to visualize Spotify song Data. We have 2 main files :
1. pipeline_spotify.py
2. dashboard.py 

## Set up 
Install the requirements on *requirements.txt* by entering the following command on the terminal
> pip  install -r requirements.txt

### Install and configure Airflow 

1. Activate your virtual environment , and run 
> pip intsall apache-airflow 
2. Call the airflow initdb command to initiate the SQLite database where Airflow will store the metadata that are necessary to manage your workflow.
3. Open the config file located in the airflow directory (cd airflow /) with the nano command and make the following modifications :<br/>
 **dags_folder** = path of the dags folder <br/>
 **load_examples** = False <br/>
 **enable_xcom_pickling** = True<br/>

You can follow the quick start guid from apache airflow http://airflow.apache.org/docs/apache-airflow/stable/start.html

3. Open two separate terminals and run :
> airflow webserver 
> airflow scheduler 

4. Navigate to the default http://localhost:8080/home local address to see the screen below:

![](https://github.com/amghita/VizSpotifyData/blob/main/img/spotify4.PNG)

5. Switch on the dag manually , Airflow Sequential Executor will immediatly run all the three tasks according to their hiearchy :

![](https://github.com/amghita/VizSpotifyData/blob/main/img/Spotify5.PNG)


**get_data** : Download spotify data from *top10s.csv* 
**data_preprocessing** : performs manipulation on spotify song data to generate top10s DF to be used in visualizations
**visualize_data** : create visualizations using Plotly


## Visualisation and Dashboard

You can now visualize the Spotify song Data by running dashboard.py

![](https://github.com/amghita/VizSpotifyData/blob/main/img/spotify1.PNG)
![](https://github.com/amghita/VizSpotifyData/blob/main/img/Spotify2.PNG)
![](https://github.com/amghita/VizSpotifyData/blob/main/img/Spotify3.PNG)




## Ressources 

1. Airflow https://airflow.apache.org/docs/
2. Guide Spotify API  https://engineering.atspotify.com/2015/03/09/understanding-spotify-web-api/
3. Plotly  https://plotly.com/python/
4. Flask  https://flask.palletsprojects.com/en/1.1.x/
