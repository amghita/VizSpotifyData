from datetime import timedelta
import datetime
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import numpy as np
import pandas as pd
import plotly.express as px
import plotly
import json
import plotly.io as pio
from flask import Flask, render_template

##### Chargement des données #######

def get_data(**context):

    data = pd.read_csv('/mnt/c/Users/ghita/PycharmProjects/Spotify-AirflowF/dags/top10s.csv',encoding="ISO-8859-1")
    context['task_instance'].xcom_push(key='dataframeSpotify',value=data)
    data.head()
    data.info()
    return data

def data_preprocessing(**context):
    df= context['task_instance'].xcom_pull(task_ids='get_data',key='dataframeSpotify')

    # supprimer id column
    df2015 = df.iloc[:, 1:15]
    df2015 = df2015.loc[df['year'] >= 2015]
    context['task_instance'].xcom_push(key='df_2015', value=df2015)
    # on prends les données des années après 2015
    print(df2015.head())
    print('Data frame shape: {}'.format(df2015.shape))

    ##### Data preprocessing ########

    famous_genres = df2015['top genre'].value_counts().head(5).to_frame().reset_index() #to
    context['task_instance'].xcom_push(key='famousgenre', value=famous_genres)
    famous_genres.columns = ['genre', 'Count']
    famous_genres_list = list(famous_genres['genre'])
    top_5_genre = famous_genres_list
    df_top = df2015.loc[df2015['top genre'].isin(top_5_genre)] #to
    context['task_instance'].xcom_push(key='dftop', value=df_top)
    group_by_genre = df_top.groupby(["year", "top genre"]).mean().sort_values('year').reset_index() #to
    context['task_instance'].xcom_push(key='groupbygenre', value=group_by_genre)
    famous_artist = df2015['artist'].value_counts().head(5).to_frame().reset_index()
    famous_artist.columns = ['artist', 'Count'] #to
    context['task_instance'].xcom_push(key='famousartistcolumns', value=famous_artist.columns)
    famous_artist_list = list(famous_artist['artist'])
    top_5_artist = famous_artist_list
    df_top_artist = df2015.loc[df2015['artist'].isin(top_5_artist)] #to
    context['task_instance'].xcom_push(key='dftopartist', value=df_top_artist)
    return famous_genres,df_top,group_by_genre,famous_artist.columns,df_top_artist


##### Dashboard ########
def dashboard(**context):
    pio.renderers.default = "browser"

    app = Flask(__name__, template_folder='templates')



    # Importation des Données du task precedent (pull)
    famous_genres1= context['task_instance'].xcom_pull(task_ids='data_preprocessing',key='famousgenre')
    group_by_genre1= context['task_instance'].xcom_pull(task_ids='data_preprocessing',key='groupbygenre')
    famous_artist1= context['task_instance'].xcom_pull(task_ids='data_preprocessing',key='famousartistcolumns')
    df1= context['task_instance'].xcom_pull(task_ids='data_preprocessing',key='df_2015')
    df_top_artist1= context['task_instance'].xcom_pull(task_ids='data_preprocessing',key='dftopartist')
    df_top1=context['task_instance'].xcom_pull(task_ids='data_preprocessing',key='dftop')

    ##### Visualisations ######

    df = pd.read_csv('/mnt/c/Users/ghita/PycharmProjects/Spotify-AirflowF/dags/top10s.csv', encoding="ISO-8859-1")
    # supprimer id column
    df = df.iloc[:, 1:15]
    df = df.loc[df['year'] >= 2015]
    # on prends les données de 5 années
    print(df.head())
    print('Data frame shape: {}'.format(df.shape))
    ##### Data preprocessing ########
    famous_genres = df['top genre'].value_counts().head(5).to_frame().reset_index()
    famous_genres.columns = ['genre', 'Count']
    famous_genres_list = list(famous_genres['genre'])
    top_5_genre = famous_genres_list
    df_top = df.loc[df['top genre'].isin(top_5_genre)]
    group_by_genre = df_top.groupby(["year", "top genre"]).mean().sort_values('year').reset_index()
    famous_artist = df['artist'].value_counts().head(5).to_frame().reset_index()
    famous_artist.columns = ['artist', 'Count']
    famous_artist_list = list(famous_artist['artist'])
    top_5_artist = famous_artist_list
    df_top_artist = df.loc[df['artist'].isin(top_5_artist)]
    def create_fig1():
        fig1 = px.bar(famous_genres,
                      x='genre',
                      y='Count',
                      title='Top 5 Genres',
                      template='plotly_white')
        return fig1

    fig1 = create_fig1()

    def create_fig2():
        fig2 = px.line(group_by_genre,
                       x='year',
                       y='pop',
                       line_group='top genre',
                       title='Top Genres Average Popularity',
                       template='plotly_white',
                       color='top genre')
        return fig2

    fig2 = create_fig2()

    def create_fig3():
        # Visualize
        fig3 = px.bar(famous_artist.sort_values('Count'),
                      x='Count',
                      y='artist',
                      title='Top 5 Artist',
                      template='plotly_white',
                      orientation='h')
        return fig3

    fig3 = create_fig3()

    def create_fig4():
        fig4 = px.violin(df, y='dnce', color='year', points='all', hover_name='title', hover_data=['artist'])
        return fig4

    fig4 = create_fig4()

    def create_fig5():
        # Average Popularity of a particular genre over the years
        fig5 = px.box(df_top_artist,
                      x='artist',
                      y='pop',
                      hover_name='title',
                      title='Artist Songs Popularity Distribution',
                      template='plotly_white',
                      points='all')
        return fig5

    fig5 = create_fig5()

    def create_fig6():
        fig6 = px.scatter(df_top,
                          x='pop',
                          y='bpm',
                          color='top genre')
        return fig6

    fig6 = create_fig6()

    @app.route("/")
    def index():
        figures = []
        figures.append(fig1)
        figures.append(fig2)
        figures.append(fig3)
        figures.append(fig4)
        figures.append(fig5)
        figures.append(fig6)

        ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]
        figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('index.html', ids=ids, figuresJSON=figuresJSON)

    if __name__ == "__main__":
        result = app.run(debug=True, port=5000)
        print(result)


######### CONFIG AIRFLOW ###########
default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'depends_on_past': False,
    'email': ['amalghita98@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # 'end_date': datetime(2018, 12, 30),
    #'retries': 1,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    #'retry_delay': timedelta(minutes=5),
    }

dag = DAG(
    dag_id= 'spotify_pipelineF',
    start_date= airflow.utils.dates.days_ago(2),
    default_args=default_args,
    description='Visualiser les données de Spotify',
    #schedule_interval=timedelta(days=1),
)

get_data = PythonOperator(
    task_id='get_data',
    python_callable = get_data,
    #xcom_push=True,
    #provide_context=True,
    dag=dag,
)

data_preprocessing = PythonOperator(
    task_id='data_preprocessing',
    python_callable = data_preprocessing,
    #xcom_push=True,
    #provide_context=True,
    dag=dag,
)

Visualize_data = PythonOperator(
    task_id ='visualize_data',
    python_callable = dashboard,
    #provide_context=True,
    dag=dag,
)

get_data >> data_preprocessing >> Visualize_data