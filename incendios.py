#----------------------------LIBRERIAS-----------------------------#

#SI NO  SE IMPORTA PIP INSTALL ...
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import  plotly_express as px
import plotly.graph_objects as go

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import jinja2

# mapas interactivos
# import folium
# from folium.plugins import FastMarkerCluster
# from folium import Choropleth
# import geopandas as gpd
# from branca.colormap import LinearColormap
# from streamlit_folium import folium_static
import streamlit.components.v1 as components


#to make the plotly graphs
# import chart_studio.plotly as py
# from plotly.offline import iplot, init_notebook_mode
# import cufflinks
# cufflinks.go_offline(connected=True)
# # init_notebook_mode(connected=True)

import plotly.express as px
# from branca import colormap
# import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# #text mining
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# from wordcloud import WordCloud
# from streamlit_folium import st_folium
# from streamlit_option_menu import option_menu

#python3 -m streamlit run incendios.py
#-----------------------------------------------------------------------------------header------------------------------------------------------------#
st.set_page_config(page_title='incendies', layout='wide',page_icon='🔥')



st.image("img/Captura de pantalla 2023-04-22 104614.png",width=1000, use_column_width=True)

st.markdown("<header><h1 style='font-size: 80px;text-align:center; color: white; opacity:0.8'><u>FOREST FIRE  IN EUROPE</u></h1></header>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white; opacity:0.8'><center>Pilar Castellano</center></h4>", unsafe_allow_html=True)

# st.divider()
#---------------------------------------------------------------READ CSV---------------------------------------------------------------------------------------#
dfm=pd.read_csv(r'data/dfprueba.csv')
# Creamos el Menú horizontal
filtro_year=st.sidebar.selectbox('AÑO', dfm["YEAR"].unique())
# --------------------------------------------------------------DATOS mapa-------------------------------------------------------------------------------------#
lats2018 = dfm['LATITUD'].tolist() #guardamos la latitud
lons2018 = dfm['LONGITUD'].tolist()#guarfdamos longitudes
locations = list(zip(lats2018, lons2018))
meanlat,meanlong=dfm['LATITUD'].mean(),dfm['LONGITUD'].mean()


#------------------------------------ mapa --------------------------#
st.markdown("<h4 style='text-align: center; color: blue; opacity:0.8'><center>ANALISIS GEOGRAFICO</center></h4>", unsafe_allow_html=True)
col1,col2=st.columns(2)
with col1: 
    fig = px.density_mapbox(dfm, lat='LATITUD', lon='LONGITUD',radius=3,width=600,height=510,
                        center=dict(lat=meanlat, lon=meanlong), zoom=2,opacity=0.5,
                        mapbox_style="stamen-terrain",color_continuous_scale = 'rainbow')
    fig.update_coloraxes(showscale=False)
    fig
with col2:
    fig = px.scatter(dfm, x="YEAR", y="AREA_HA", color="Name", hover_name="Name",size='AREA_HA', template='plotly_dark',
                 title="Áreas quemadas por incendios forestales en EU (2000-2023)")
    fig

 # -------------------------------------distribucion de incendios en funcion de ha-------------------------#     
col1,col2=st.columns(2)
with col1:  
    # fig = px.scatter(dfm, x='AREA_HA',  color='AREA_HA',title='incendios por ha quemadas ',
    #                opacity=0.8,
    #                template='plotly_dark',width=800, height=500)
    # fig
    Incendiopais=dfm['Name'].value_counts()
    Incendiopais=Incendiopais[Incendiopais>300]
    fig = px.pie( values=Incendiopais.values, names=Incendiopais.index,  template='plotly_dark', title='Paises con más número de incendios')
    fig
# --------------------------------------------------------------ha quemadas acomulativas--------------#
with col2:
        # incendiocountry=dfm['Name'].value_counts()
        # sumpais=dfm.groupby('Name').sum()
        # sumpais['cantidad_incendios']=incendiocountry
        # sumpais['medias']= sumpais['AREA_HA']/ sumpais['cantidad_incendios']
        # fig = px.bar(sumpais, x=sumpais.index, y='medias',template='plotly_dark',title='media ha quemada por incendio y pais')
        # fig
        
        dfacoi=dfm[['Name','AREA_HA','YEAR']]
        dfaco=dfacoi.groupby(['Name','YEAR']).sum()
        df_acumulado = dfaco.groupby('Name')['AREA_HA'].cumsum().reset_index()
        dfacc=df_acumulado[df_acumulado['AREA_HA']>300000]
        fig = px.line(dfacc, x="YEAR", y='AREA_HA', color='Name',template='plotly_dark',width=800, height=500,title='Superficie acomulada quemada')
        fig


# -------------------------------------------------------------porcentaje area quemada del pais-------#
dfkm2=pd.read_csv('data/paiseslandcoverHA.csv')
dfkm2['percentage'] = dfkm2['AREA_HA']*(100/dfkm2['Total'])

barchart=px.bar(dfkm2,x=dfkm2['COUNTRY'],y=dfkm2['Total'],width=1500, height=500,color=dfkm2['percentage'],template='plotly_dark',
                text=dfkm2['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)),title='Porcentaje de superficie quemada')
barchart



st.markdown("<h4 style='text-align: center; color: blue; opacity:0.8'><center>ANALISIS TEMPORAL</center></h4>", unsafe_allow_html=True)
# --------------------------------------------------------------ha por año-------#
sumaño=dfm.groupby('YEAR').sum()

# --------------------------------------------------------------nº incendios por año-------#
incendioYear=dfm['YEAR'].value_counts()

# --------------------------------------------------------------has quemasdas de media por incendio y año-------#
sumaño['cantidad_incendios']=incendioYear
sumaño['medias']= sumaño['AREA_HA']/ sumaño['cantidad_incendios']
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{}, {}],
           [{"colspan": 2}, None]],
    subplot_titles=("Número de incendios totales por año","Superficie total por año", "Media de superficie por incendio y año"))

fig.add_trace(go.Bar(x=incendioYear.index,y=incendioYear.values),
                 row=1, col=1)
fig.add_trace(go.Bar(x=sumaño.index, y=sumaño['AREA_HA']),
              row=1, col=2)
fig.add_trace(go.Scatter(x=sumaño.index, y=sumaño['medias']),row=2, col=1)

fig.update_layout(showlegend=False, template='plotly_dark',width=1500, height=500)
fig




# -------------------------------------------------------------porcentaje area quemada por mes------#

dfmeses=dfm[(dfm['YEAR']<=filtro_year)&(dfm['YEAR']>2000)]
dfmeses=dfmeses[['YEAR','MONTH']]
dfmeses=pd.DataFrame(dfmeses.value_counts())
dfmeses = dfmeses.reset_index(level=['YEAR','MONTH'])
dfmeses=dfmeses.sort_values(by=['YEAR','MONTH'])
fig = px.line(dfmeses, x="MONTH", y=0, color='YEAR',template='plotly_dark',width=1500, height=500)
fig


