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





#python -m streamlit run incendios.py
#-----------------------------------------------------------------------------------header------------------------------------------------------------#
st.set_page_config(page_title='incendies', layout='wide',page_icon='🔥')
dfm=pd.read_csv(r'data/dfpruebaHA.csv')
#-----------------------------------------------------------------------------------header------------------------------------------------------------#
#-----------------------------------SECCION DE PESTAÑAS----------------------------#
tab1, tab2= st.tabs (["provincia",'pais'])    

#----------------------------------slide bar-----------------------------------------# 

filtro_pais = st.sidebar.selectbox("PAIS", dfm["Name"].unique())
filtro_procinvia= st.sidebar.selectbox("PROVINCIA", dfm[dfm['Name']==filtro_pais]['PROVINCE'].unique())
filtro_año= st.sidebar.selectbox("PROVINCIA", dfm[dfm['PROVINCE']==filtro_procinvia]['YEAR'].unique())
agree = st.sidebar.checkbox('todos los años, de todo el pais')
#------------------------------------------------------------------------------------map------------
with tab1:
    col1,col2=st.columns(2)
    with col1:   
            dffire=dfm[(dfm['Name']==filtro_pais)&(dfm['PROVINCE']==filtro_procinvia)&(dfm['YEAR']==filtro_año)]
            lats2018 =dffire['LATITUD'].tolist() #guardamos la latitud
            lons2018 = dffire['LONGITUD'].tolist()#guarfdamos longitudes
            locations = list(zip(lats2018, lons2018))
            meanlat,meanlong=dffire['LATITUD'].mean(),dffire['LONGITUD'].mean()
            fig = px.density_mapbox(dffire, lat='LATITUD', lon='LONGITUD',radius=10,width=600,height=510,
                            center=dict(lat=meanlat, lon=meanlong), zoom=6,opacity=1,
                            mapbox_style="stamen-terrain",color_continuous_scale = 'Turbo')
            fig.update_coloraxes(showscale=False)
            fig
            
    with col2:
        st.markdown('')
        
        provsum =dffire[['AREA_HA', 'BROADLEAVED', 'CONIFER', 'MIXED', 'SCLEROPHYLLOUS',
        'TRANSITIONAL', 'OTHERNATLC', 'AGRIAREAS', 'ARTIFSURF', 'OTHERLC',
        '%NAT2000']].sum()

        # Crear un nuevo DataFrame con las sumas
        sums_df = pd.DataFrame({'Sumas': provsum})
        fig=px.bar(sums_df,x=sums_df.index,y=sums_df['Sumas'] ,template='plotly_dark')
        fig

with tab2:
    
    col1,col2=st.columns(2)
    with col1:
                dfallincendios=dfm[dfm['Name']==filtro_pais]
                lats2018 =dfallincendios['LATITUD'].tolist() #guardamos la latitud
                lons2018 = dfallincendios['LONGITUD'].tolist()#guarfdamos longitudes
                locations = list(zip(lats2018, lons2018))
                meanlat,meanlong=dfallincendios['LATITUD'].mean(),dfallincendios['LONGITUD'].mean()
                fig = px.density_mapbox(dfallincendios, lat='LATITUD', lon='LONGITUD',width=600,height=510,
                                center=dict(lat=meanlat, lon=meanlong), zoom=3,opacity=1,radius=3,
                                mapbox_style="stamen-terrain",color_continuous_scale = 'Turbo')
                fig.update_coloraxes(showscale=False)
                fig
    with col2:
                fig=px.scatter_polar(dfallincendios, r="AREA_HA", theta=dfallincendios['YEAR'].astype('str'),
                            color="MONTH",  size=dfallincendios['YEAR'].astype('int'),template='plotly_dark',
                            color_discrete_sequence=px.colors.sequential.Plasma_r,width=500, height=500)
                fig
    col1,col2=st.columns(2)
    with col1:
        provinvias=dfallincendios['PROVINCE'].value_counts()
        provinvias=provinvias[provinvias>100]
        fig=px.bar(provinvias,x=provinvias.index,y=provinvias.values ,template='plotly_dark', title='numero de incendios')
        fig
    
    with col2:
        fig = px.bar(dfallincendios, x="YEAR", y="AREA_HA", color="MONTH",template='plotly_dark', title='numero de incendios')
        fig
