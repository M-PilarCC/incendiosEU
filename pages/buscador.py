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



#python -m streamlit run incendios.py

#-----------------------------------------------------------------------------------header------------------------------------------------------------#
st.set_page_config(page_title='incendies', layout='wide',page_icon='🔥')
st.image("img/inc4.png",width=500, use_column_width=True)
dfm=pd.read_csv(r'data/dfpruebaHA.csv')
#-----------------------------------------------------------------------------------header------------------------------------------------------------#
#-----------------------------------SECCION DE PESTAÑAS----------------------------#
tab1, tab2= st.tabs (["provincia",'pais'])    

#----------------------------------slide bar-----------------------------------------# 

filtro_pais = st.sidebar.selectbox("PAIS", dfm["Name"].unique())
filtro_procinvia= st.sidebar.selectbox("PROVINCIA", dfm[dfm['Name']==filtro_pais]['PROVINCE'].unique())
filtro_año= st.sidebar.selectbox("PROVINCIA", dfm[dfm['PROVINCE']==filtro_procinvia]['YEAR'].unique())

#------------------------------------------------------------------------------------map------------
with tab1:
    
    st.markdown("<h4 style='text-align: center; background-color: orange; opacity:0.8'><center>TODOS LOS INCENDIOS POR PROVINCIA Y AÑO</center></h4>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:   
            dffire=dfm[(dfm['Name']==filtro_pais)&(dfm['PROVINCE']==filtro_procinvia)&(dfm['YEAR']==filtro_año)]
            lats2018 =dffire['LATITUD'].tolist() #guardamos la latitud
            lons2018 = dffire['LONGITUD'].tolist()#guarfdamos longitudes
            locations = list(zip(lats2018, lons2018))
            meanlat,meanlong=dffire['LATITUD'].mean(),dffire['LONGITUD'].mean()
            fig = px.density_mapbox(dffire, lat='LATITUD', lon='LONGITUD',radius=10,width=600,height=500,
                            center=dict(lat=meanlat, lon=meanlong), zoom=6,opacity=1,
                            mapbox_style="stamen-terrain",color_continuous_scale = 'Turbo')
            fig.update_coloraxes(showscale=False)
            fig
            
    with col2:
        st.markdown('')
        
        provsum =dffire[['AREA_HA', 'BROADLEAVED', 'CONIFER', 'MIXED', 'SCLEROPHYLLOUS',
        'TRANSITIONAL', 'OTHERNATLC', 'AGRIAREAS', 'ARTIFSURF', 'OTHERLC',
        'NAT2000']].sum()

        
        sums_df = pd.DataFrame({'Sumas': provsum})
        fig=px.bar(sums_df,x=sums_df.index,y=sums_df['Sumas'] ,template='plotly_dark',width=500,height=500,color=sums_df['Sumas'] , title=' Superficie total, cantidad de cada tipo, y cantidad de superficie de red natura quemada.')
        fig.update_coloraxes(showscale=False)
        fig

with tab2:
    st.markdown("<h4 style='text-align: center; background-color: orange; opacity:0.8'><center>INCENDIOS ÚLTIMOS 13 AÑOS POR PAÍS</center></h4>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        
                dfallincendios=dfm[dfm['Name']==filtro_pais]
                dfallincendios=dfallincendios[dfallincendios['YEAR']>2010]
                lats2018 =dfallincendios['LATITUD'].tolist() #guardamos la latitud
                lons2018 = dfallincendios['LONGITUD'].tolist()#guarfdamos longitudes
                locations = list(zip(lats2018, lons2018))
                meanlat,meanlong=dfallincendios['LATITUD'].mean(),dfallincendios['LONGITUD'].mean()
                fig = px.density_mapbox(dfallincendios, lat='LATITUD', lon='LONGITUD',width=600,height=510,
                                center=dict(lat=meanlat, lon=meanlong), zoom=3,opacity=1,radius=3,
                                mapbox_style="stamen-terrain",color_continuous_scale = 'Turbo')
                fig.update_coloraxes(showscale=False)
                fig.update_layout(showlegend=False)
                fig
    with col2:
            
            fig=px.scatter_polar(dfallincendios, r="AREA_HA", theta=dfallincendios['YEAR'].astype('str'),
                            color=dfallincendios['YEAR'].astype('str'),  size=dfallincendios['YEAR'],template='plotly_dark',
                            color_discrete_sequence=px.colors.sequential.Plasma_r,width=500, height=500)
            fig.update_coloraxes(showscale=False)
            fig.update_layout(showlegend=False)
            fig
            
            
    col1,col2=st.columns(2)
    with col1:
        provinvias=dfallincendios['PROVINCE'].value_counts()
        provinvias=provinvias[provinvias>100]
        fig=px.bar(provinvias,x=provinvias.index,y=provinvias.values ,template='plotly_dark',width=500,height=500,color=provinvias.index ,title='¿que provincias se han quemado mas?')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(showlegend=False)
        fig.update_xaxes(tickangle=45)
        fig
    
    with col2:
            # Cambiar el índice por los nombres de los meses
        nombres_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        # Mostrar los datos con el nuevo índice
        
        incendiomonth=dfallincendios['MONTH'].value_counts().sort_index()
        incendiomonth.rename(index=dict(zip(range(1,13), nombres_meses)),inplace=True)
        fig = px.bar(incendiomonth, x=incendiomonth.index,y=incendiomonth.values, color=incendiomonth.values,template='plotly_dark',width=500,height=500)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(showlegend=False)
        fig

        
  
    fig = px.scatter_mapbox(dfallincendios,lon = 'LONGITUD',
        lat = 'LATITUD',     color='MONTH',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=5,height=500,width=500)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(showlegend=False)
    fig.update_coloraxes(showscale=False)
    fig
