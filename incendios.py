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


import streamlit.components.v1 as components

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#python3 -m streamlit run incendios.py
#-----------------------------------------------------------------------------------header------------------------------------------------------------#
st.set_page_config(page_title='incendies', layout='wide',page_icon='🔥')

st.image("img/inc4.png",width=500, use_column_width=True)

#---------------------------------------------------------------READ CSV---------------------------------------------------------------------------------------#
dfm=pd.read_csv(r'data/dfprueba.csv')

# --------------------------------------------------------------DATOS mapa-------------------------------------------------------------------------------------#
lats2018 = dfm['LATITUD'].tolist() #guardamos la latitud
lons2018 = dfm['LONGITUD'].tolist()#guarfdamos longitudes
locations = list(zip(lats2018, lons2018))
meanlat,meanlong=dfm['LATITUD'].mean(),dfm['LONGITUD'].mean()


#------------------------------------ mapa --------------------------#
st.markdown("<h4 style='text-align: center; background-color:  orange; opacity:0.8'><center>ANÁLISIS GEOGRÁFICO</center></h4>", unsafe_allow_html=True)
col1,col2=st.columns(2)
with col1: 
    fig = px.density_mapbox(dfm, lat='LATITUD', lon='LONGITUD',radius=3,width=600,height=510,
                        center=dict(lat=meanlat, lon=meanlong), zoom=2,opacity=0.5,
                        mapbox_style="stamen-terrain",color_continuous_scale = 'rainbow')
    fig.update_coloraxes(showscale=False)
    fig
with col2:
    fig = px.scatter(dfm, x="YEAR", y="AREA_HA", color="Name", hover_name="Name",size='AREA_HA', template='plotly_dark',width=750,height=550,
                 title="Áreas quemadas por incendios forestales en EU (2000-2023)")
    fig

 # -------------------------------------Paises con mas numero de incendios-------------------------#     
col1,col2=st.columns(2)
with col1:  
    Incendiopais=dfm['Name'].value_counts()
    Incendiopais=Incendiopais[Incendiopais>300]
    fig = px.pie( values=Incendiopais.values, names=Incendiopais.index,  template='plotly_dark', title='¿Donde ocurren más incendios? +300',width=600,height=510)
    fig
# --------------------------------------------------------------ha quemadas acomulativas--------------#
with col2:
        dfacoi=dfm[['Name','AREA_HA','YEAR']]
        dfaco=dfacoi.groupby(['Name','YEAR']).sum()
        df_acumulado = dfaco.groupby('Name')['AREA_HA'].cumsum().reset_index()
        dfacc=df_acumulado[df_acumulado['AREA_HA']>300000]
        fig = px.line(dfacc, x="YEAR", y='AREA_HA', color='Name',template='plotly_dark',width=750,height=550,title='qué paises tienen mas superficie quemada')
        fig


# -------------------------------------------------------------porcentaje area quemada del pais-------#
dfkm2=pd.read_csv('data/paiseslandcoverHA.csv')
dfkm2['percentage'] = dfkm2['AREA_HA']*(100/dfkm2['Total'])

barchart=px.bar(dfkm2,x=dfkm2[' name'],y=dfkm2['Total'],width=1300, height=500,color=dfkm2['percentage'],template='plotly_dark',
                text=dfkm2['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)),title='Porcentaje de superficie quemada')
barchart.update_layout(showlegend=True)
barchart


st.title('')
st.markdown("<h4 style='text-align: center; background-color:  orange; opacity:0.8'><center>ANÁLISIS TEMPORAL</center></h4>", unsafe_allow_html=True)
st.title('')
# --------------------------------------------------------------ha por año-------#
sumaño=dfm.groupby('YEAR').sum()

# --------------------------------------------------------------nº incendios por año-------#
incendioYear=dfm['YEAR'].value_counts()

# --------------------------------------------------------------has quemasdas de media por incendio y año-------#
sumaño['cantidad_incendios']=incendioYear
sumaño['medias']= sumaño['AREA_HA']/ sumaño['cantidad_incendios']
sumaño['medias']=sumaño['medias'].round(1)
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

fig.update_layout(showlegend=False, template='plotly_dark',width=1300, height=500)
fig





st.title('')
st.markdown("<h4 style='text-align: center; background-color:  orange; opacity:0.8'><center>ANÁLISIS SUPERFICIE QUEMADA</center></h4>", unsafe_allow_html=True)
st.title('')


col=[ 'BROADLEAVED', 'CONIFER', 'MIXED',
       'SCLEROPHYLLOUS', 'TRANSITIONAL', 'OTHERNATLC', 'AGRIAREAS',
       'ARTIFSURF', 'OTHERLC']
dfm["categoria_mayor"] = dfm[col].idxmax(axis=1)
tipovege=dfm["categoria_mayor"] .value_counts()
fig = px.pie( values=tipovege.values, names=tipovege.index, template='plotly_dark',title='Tipo de vegeaticon mayoritaria en la superficie quemada')
fig


bosque=dfm[(dfm['categoria_mayor']=='BROADLEAVED')| (dfm['categoria_mayor']=='CONIFER')|(dfm['categoria_mayor']=='MIXED')]
sumañobosque=bosque.groupby('YEAR').sum()
incendioYearbosque=bosque['YEAR'].value_counts()
sumañobosque['cantidad_incendios']=incendioYearbosque
sumañobosque['mediasb']= sumañobosque['AREA_HA']/ sumañobosque['cantidad_incendios']
sumañobosque['mediasb']=sumañobosque['mediasb'].round(1)

agri=dfm[dfm['categoria_mayor']=='AGRIAREAS']
sumaño=agri.groupby('YEAR').sum()
incendioYear=agri['YEAR'].value_counts()
sumaño['cantidad_incendios']=incendioYear
sumaño['mediasag']= sumaño['AREA_HA']/ sumaño['cantidad_incendios']
sumaño['mediasag']=sumaño['mediasag'].round(1)


scler=dfm[dfm['categoria_mayor']=='SCLEROPHYLLOUS']
sumañoscler=scler.groupby('YEAR').sum()
incendioYearscler=scler['YEAR'].value_counts()
sumañoscler['cantidad_incendios']=incendioYearscler
sumañoscler['mediasscler']= sumañoscler['AREA_HA']/ sumañoscler['cantidad_incendios']
sumañoscler['mediasscler']=sumañoscler['mediasscler'].round(1)

trans=dfm[dfm['categoria_mayor']=='TRANSITIONAL']
sumañotrans=trans.groupby('YEAR').sum()
incendioYeartrans=trans['YEAR'].value_counts()
sumañotrans['cantidad_incendios']=incendioYeartrans
sumañotrans['mediastrans']= sumañotrans['AREA_HA']/ sumañotrans['cantidad_incendios']
sumañotrans['mediastrans']=sumañotrans['mediastrans'].round(1)

other=dfm[dfm['categoria_mayor']=='OTHERNATLC']
sumañoother=other.groupby('YEAR').sum()
incendioYearother=other['YEAR'].value_counts()
sumañoother['cantidad_incendios']=incendioYeartrans
sumañoother['mediasother']= sumañoother['AREA_HA']/ sumañoother['cantidad_incendios']
sumañoother['mediasother']=sumañoother['mediasother'].round(1)
df_concatenado = pd.concat([sumaño, sumañobosque['mediasb'],sumañoscler['mediasscler'],sumañotrans['mediastrans'],sumañoother['mediasother']], axis=1)
fig = px.line(df_concatenado, x=df_concatenado.index, y=['mediasag', 'mediasb',
       'mediasscler', 'mediastrans', 'mediasother'],template='plotly_dark')
fig