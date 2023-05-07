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

#Datos
def data():
    dfm=pd.read_csv(r'data/dfpruebaHA.csv')
    return dfm
dfm=data()

#SECCION DE PESTAÑAS
tab1, tab2= st.tabs (["provincia",'pais'])    

#Slide bar
#pais se puede usar en las dos pestañas
filtro_pais = st.sidebar.selectbox("PAIS", dfm["Name"].unique())
#los filtros de provincia y año son para la primera pestaña
filtro_procinvia= st.sidebar.selectbox("PROVINCIA", dfm[dfm['Name']==filtro_pais]['PROVINCE'].unique())
filtro_año= st.sidebar.selectbox("PROVINCIA", dfm[dfm['PROVINCE']==filtro_procinvia]['YEAR'].unique())



#Pestaña 1, PROVINCIA
with tab1:
    #titulo
    st.markdown("<h4 style='text-align: center; background-color: orange; opacity:0.8'><center>TODOS LOS INCENDIOS POR PROVINCIA Y AÑO</center></h4>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:   
            # heat box de incendios
            dffire=dfm[(dfm['Name']==filtro_pais)&(dfm['PROVINCE']==filtro_procinvia)&(dfm['YEAR']==filtro_año)]
            lats2018 =dffire['LATITUD'].tolist() 
            lons2018 = dffire['LONGITUD'].tolist()
            locations = list(zip(lats2018, lons2018))
            #sacamos la media de las latitudes y las longitudes para centrar el mapa automaticamente
            meanlat,meanlong=dffire['LATITUD'].mean(),dffire['LONGITUD'].mean()
            
            fig = px.density_mapbox(dffire, lat='LATITUD', lon='LONGITUD',radius=10,width=600,height=500,
                            center=dict(lat=meanlat, lon=meanlong), zoom=6,opacity=1,
                            mapbox_style="stamen-terrain",color_continuous_scale = 'Turbo')
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
    with col2:
        st.markdown('')
        #hacemos una suma de los tipos de superficies de los incendios
        provsum =dffire[['AREA_HA', 'BROADLEAVED', 'CONIFER', 'MIXED', 'SCLEROPHYLLOUS',
        'TRANSITIONAL', 'OTHERNATLC', 'AGRIAREAS', 'ARTIFSURF', 'OTHERLC',
        'NAT2000']].sum()

        #grafico de barras cantidad de superficie de cada tipo
        sums_df = pd.DataFrame({'Sumas': provsum})
        fig=px.bar(sums_df,x=sums_df.index,y=sums_df['Sumas'] ,template='plotly_dark',width=500,height=500,color=sums_df['Sumas'] , title=' Superficie total, cantidad de cada tipo, y cantidad de superficie de red natura quemada.')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig,use_container_width=True)
        
        
        
#Pestaña 2, PAIS
with tab2:
    
    st.markdown("<h4 style='text-align: center; background-color: orange; opacity:0.8'><center>INCENDIOS ÚLTIMOS 13 AÑOS POR PAÍS</center></h4>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        # heat map incendios todo el pais
        dfallincendios=dfm[dfm['Name']==filtro_pais]
        dfallincendios=dfallincendios[dfallincendios['YEAR']>2010]
        lats2018 =dfallincendios['LATITUD'].tolist() 
        lons2018 = dfallincendios['LONGITUD'].tolist()
        locations = list(zip(lats2018, lons2018))
        meanlat,meanlong=dfallincendios['LATITUD'].mean(),dfallincendios['LONGITUD'].mean()
        fig = px.density_mapbox(dfallincendios, lat='LATITUD', lon='LONGITUD',width=600,height=510,
                                center=dict(lat=meanlat, lon=meanlong), zoom=3,opacity=1,radius=3,
                                mapbox_style="stamen-terrain",color_continuous_scale = 'Turbo')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        
        
    with col2:
        #scatterpolar chart  donde la orientacion es el año y el radio es la cantidad de superficie quemada
        fig=px.scatter_polar(dfallincendios, r="AREA_HA", theta=dfallincendios['YEAR'].astype('str'),
                            color=dfallincendios['YEAR'].astype('str'),  size=dfallincendios['YEAR'],template='plotly_dark',
                            color_discrete_sequence=px.colors.sequential.Plasma_r,width=500, height=500)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
            
            
            
    col1,col2=st.columns(2)
    with col1:
        #grafico de barras cantidad de incendios por provincias
        provinvias=dfallincendios['PROVINCE'].value_counts()
        provinvias=provinvias[provinvias>100]
        fig=px.bar(provinvias,x=provinvias.index,y=provinvias.values ,template='plotly_dark',color=provinvias.values,width=500,height=500,title='¿qué provincias se han quemado más?')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_title='',yaxis_title=' ',showlegend=False)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig,use_container_width=True)
    
    
    with col2:
        #grafico de barras de cantidad de incendios por meses
        # Cambiar el índice por los nombres de los meses
        nombres_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        # Mostrar los datos con el nuevo índice
        incendiomonth=dfallincendios['MONTH'].value_counts().sort_index()
        
        #hacemos un diccionario para que cambie cada numero por su nombre de mes correspondiente
        incendiomonth.rename(index=dict(zip(range(1,13), nombres_meses)),inplace=True)
        fig = px.bar(incendiomonth, x=incendiomonth.index,y=incendiomonth.values, color=incendiomonth.values,template='plotly_dark',width=500,height=500,title='Cantidad de incendios por meses')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_title='',yaxis_title=' ',showlegend=False)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig,use_container_width=True)

        
   # scatter map donde los colores se refieren a los meses de ocurriencia
    fig = px.scatter_mapbox(dfallincendios,lon = 'LONGITUD',
        lat = 'LATITUD',     color='MONTH',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=5,height=500,width=500)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(showlegend=True)
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig,use_container_width=True)
