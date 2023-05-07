#----------------------------LIBRERIAS-----------------------------#
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import  plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import streamlit.components.v1 as components


#Encabezado de pagina
st.set_page_config(page_title='IncendiosEU', layout='wide',page_icon='🔥')
st.image("img/inc4.png",width=500, use_column_width=True)

#Data
def data():
    dfm=pd.read_csv(r'data/dfprueba.csv')
    dfkm2=pd.read_csv('data/paiseslandcoverHA.csv')
    return dfm, dfkm2

dfm,dfkm2 = data()


#Data origen (sidebar)
agree = st.sidebar.checkbox('para ver la web origen de los datos')
if agree:
    st.sidebar.write('https://effis.jrc.ec.europa.eu/')
    



#ANALISIS GEOGRÁFICO
st.markdown("<h4 style='text-align: center; background-color:  orange; opacity:0.8'><center>ANÁLISIS GEOGRÁFICO</center></h4>", unsafe_allow_html=True)
col1,col2=st.columns(2)


# heat map incendios 
lats2018 = dfm['LATITUD'].tolist() #guardamos la latitud
lons2018 = dfm['LONGITUD'].tolist()#guarfdamos longitudes
locations = list(zip(lats2018, lons2018))
meanlat,meanlong=dfm['LATITUD'].mean(),dfm['LONGITUD'].mean()

with col1: 
    fig = px.density_mapbox(dfm, lat='LATITUD', lon='LONGITUD',radius=3,width=600,height=510,
                        center=dict(lat=meanlat, lon=meanlong), zoom=2,opacity=0.5,
                        mapbox_style="stamen-terrain",color_continuous_scale = 'rainbow')
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig,use_container_width=True)
    
    
# scatterplot de incendios
with col2:
    fig = px.scatter(dfm, x="YEAR", y="AREA_HA", color="Name", hover_name="Name",size='AREA_HA', template='plotly_dark',width=750,height=550,
                 title="Áreas quemadas por incendios forestales en EU (2000-2023)")
    st.plotly_chart(fig,use_container_width=True)

# Pie chart número de incendios con paises de mas de 300 icendios 
col1,col2=st.columns(2)
with col1:  
    Incendiopais=dfm['Name'].value_counts()
    Incendiopais=Incendiopais[Incendiopais>300]
    colores = px.colors.sequential.YlOrRd_r
    fig = px.pie( values=Incendiopais.values, names=Incendiopais.index,  template='plotly_dark', title='¿Donde ocurren más incendios? +300',width=600,height=510,color_discrete_sequence=colores)
    st.plotly_chart(fig,use_container_width=True)
    
# Grafico de lineas de areas acomuladas
with col2:
        dfacoi=dfm[['Name','AREA_HA','YEAR']]
        #agrupamos por nombre del pais y por año
        dfaco=dfacoi.groupby(['Name','YEAR']).sum()
        # utilizamos el cumsum para ver la suma acomulativa
        df_acumulado = dfaco.groupby('Name')['AREA_HA'].cumsum().reset_index()
        # fijamos el minimo de area en 300.000 hectareas
        dfacc=df_acumulado[df_acumulado['AREA_HA']>300000]
        fig = px.line(dfacc, x="YEAR", y='AREA_HA', color='Name',template='plotly_dark',width=750,height=550,title='¿qué paises tienen más superficie quemada?')
        st.plotly_chart(fig,use_container_width=True)


# Grafico de barras por pais, su area y el porcentaje quemado
# pasamos datos a porcentaje
dfkm2['percentage'] = dfkm2['AREA_HA']*(100/dfkm2['Total'])
#ponemos la escala de color que deseamos
colores = px.colors.sequential.Jet[3:]
barchart=px.bar(dfkm2,x=dfkm2[' name'],y=dfkm2['Total'],width=1300, height=500,color=dfkm2['percentage'],template='plotly_dark',
                text=dfkm2['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)),title='Porcentajes de superficie total',color_continuous_scale=colores)
barchart.update_layout(showlegend=True)
barchart.update_coloraxes(showscale=False)
barchart.update_xaxes(tickangle=45)
st.plotly_chart(barchart,use_container_width=True)



#ANÁLISIS TEMPORAL
st.title('')
st.markdown("<h4 style='text-align: center; background-color:  orange; opacity:0.8'><center>ANÁLISIS TEMPORAL</center></h4>", unsafe_allow_html=True)
st.title('')

#creamos dos variables, la suma de datos por año y un value counts de incendios por año
sumaño=dfm.groupby('YEAR').sum()
incendioYear=dfm['YEAR'].value_counts()
#juntamos las variables
sumaño['cantidad_incendios']=incendioYear
#creamos una nueva columna con datos de medias
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
st.plotly_chart(fig,use_container_width=True)



#ANÁLISIS SUPERFICIE
st.title('')
st.markdown("<h4 style='text-align: center; background-color:  orange; opacity:0.8'><center>ANÁLISIS SUPERFICIE QUEMADA</center></h4>", unsafe_allow_html=True)
st.title('')

col1,col2=st.columns(2)
with col1: 
    # creamos una columna en el data frame que indique cual es de las superficies predominaba en el area quemada
    col=[ 'BROADLEAVED', 'CONIFER', 'MIXED',
           'SCLEROPHYLLOUS', 'TRANSITIONAL', 'OTHERNATLC', 'AGRIAREAS',
           'ARTIFSURF', 'OTHERLC']
    dfm["categoria_mayor"] = dfm[col].idxmax(axis=1)
    dfmpie=dfm.copy()
    #cambiamos los nombres 
    dfmpie['categoria_mayor'].replace(['BROADLEAVED', 'CONIFER', 'MIXED'], 'FOREST', inplace=True)
    dfmpie['categoria_mayor'].replace(['OTHERNATLC', 'OTHERLC'], 'NATURALIND.', inplace=True)
    #realizamos un value couns de cada categoria
    tipovege=dfmpie["categoria_mayor"] .value_counts()
    colores = px.colors.sequential.speed
    fig = px.pie( values=tipovege.values, names=tipovege.index, template='plotly_dark',title='Superficie que se han quemado',color_discrete_sequence=colores)
    st.plotly_chart(fig,use_container_width=True)
    
with col2: 
    # creamos un grafico solo con los datos de categoria forest
    fores=dfm[(dfm['categoria_mayor']=='BROADLEAVED')|(dfm['categoria_mayor']== 'CONIFER')|(dfm['categoria_mayor']== 'MIXED')]
    tipoforest=fores["categoria_mayor"] .value_counts()
    colores = px.colors.sequential.Greens_r
    fig = px.pie( values=tipoforest.values, names=tipoforest.index, template='plotly_dark',title='Bosques',color_discrete_sequence=colores)
    st.plotly_chart(fig,use_container_width=True)
    
