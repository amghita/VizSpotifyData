import pandas as pd
import numpy as np
import plotly.express as px
import plotly
import json
import plotly.io as pio
from flask import Flask, render_template

pio.renderers.default = "browser"

app = Flask(__name__,template_folder='templates')

 #####  Importation des Données #######
#use encoder to avoid utf-8 error
df = pd.read_csv('top10s.csv',encoding = "ISO-8859-1")
#supprimer id column
df = df.iloc[:,1:15]
df = df.loc[df['year']>=2015]
# on prends les données de 5 années
print(df.head())
print('Data frame shape: {}'.format(df.shape))
##### Data preprocessing ########
famous_genres = df['top genre'].value_counts().head(5).to_frame().reset_index()
famous_genres.columns = ['genre','Count']
famous_genres_list = list(famous_genres['genre'])
top_5_genre = famous_genres_list
df_top = df.loc[df['top genre'].isin(top_5_genre)]
group_by_genre = df_top.groupby(["year","top genre"]).mean().sort_values('year').reset_index()
famous_artist = df['artist'].value_counts().head(5).to_frame().reset_index()
famous_artist.columns = ['artist','Count']
famous_artist_list = list(famous_artist['artist'])
top_5_artist = famous_artist_list
df_top_artist = df.loc[df['artist'].isin(top_5_artist)]

##### Visualisations ######

def create_fig1():
    fig1= px.scatter(df, x='dnce', y='nrgy', color='nrgy', hover_name='title', hover_data=['artist', 'year'],title ='Distribution of energy and danceability')

    return fig1
fig1=create_fig1()

def create_fig2():
    fig2 = px.line(group_by_genre,
                   x='year',
                   y='pop',
                   line_group='top genre',
                   title='Top Genres Average Popularity',
                   template='plotly_white',
                   color='top genre')
    return fig2
fig2=create_fig2()

def create_fig3():
    # Visualize
    fig3 = px.bar(famous_artist.sort_values('Count'),
                  x='Count',
                  y='artist',
                  title='Top 5 Artist',
                  template='plotly_white',
                  orientation='h')
    return fig3
fig3=create_fig3()


def create_fig4():
    fig4 = px.violin(df, y='dnce', color='year', points='all', hover_name='title', hover_data=['artist'] , title='Danceability of songs')
    return fig4
fig4=create_fig4()


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
fig5=create_fig5()


def create_fig6():
    fig6= px.scatter(df_top,
                      x='pop',
                      y='bpm',
                      color='top genre',title='Distribution of popularity and BPM')
    return fig6
fig6=create_fig6()

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
    return render_template('index.html',ids=ids,figuresJSON=figuresJSON)


if __name__ == "__main__":
    print(df)
    result = app.run(debug=True,  port=5000)
    print(result)
