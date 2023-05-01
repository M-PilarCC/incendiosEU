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

# from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor



#-----------------------------------------------------------------------------------header------------------------------------------------------------#
st.set_page_config(page_title='IncendiosEU', layout='wide',page_icon='🔥')
st.image("img/inc4.png",width=500, use_column_width=True)

dfreg = pd.read_csv('data/dfreg.csv')
dicc_month={'mar':3, 'oct': 10, 'aug':8, 'sep':9, 'apr':4, 'jun':5, 'jul':6, 'feb':7, 'jan': 1,
       'dec':12, 'may':5, 'nov':11}
#-----------------------------------------------------------------------------------sidebar-------
mes = st.sidebar.selectbox("Mes del año", dicc_month.keys())
for i in dicc_month.keys():
    if mes==i:
        mes=dicc_month[i]
lluvia = st.sidebar.slider('Cantidad de lluvia',1.0, 100.0)
temp = st.sidebar.slider('Cantidad de temperatura',1.0, 60.0)
viento = st.sidebar.slider('Cantidad de viento',1.0, 100.0)
rh = st.sidebar.slider('Cantidad de humedad',1.0, 100.0)

#python -m streamlit run incendios.py
tab1, tab2= st.tabs (['panel BI','futuro'])  

#-----------------------------------------------------------------------------------POWER BI------
with tab1:
    st.title('')
 
    st.markdown(f'<div style="max-width:1024px;text-align: center;"><iframe title="Report Section" width="100%" height="500"src="https://app.powerbi.com/view?r=eyJrIjoiNzE3M2M5YmYtYjYyNy00NDg2LWI3MTUtNzI0YjQ4ODFhNjZlIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe></div>',
            unsafe_allow_html=True)



#-----------------------------------------------------------------------------------POWER BI------
with tab2:
    st.title('')
    st.markdown("<h4 style='text-align: center; background-color: orange; opacity:0.8'><center>PREDICCION SUPERFICIE </center></h4>", unsafe_allow_html=True)
    X,y=dfreg[['month','temp','RH','wind','rain']],dfreg['area'].values 
    #Instanciamos el modelo
    model = RandomForestRegressor(n_estimators=200, criterion='squared_error', max_depth=None, min_samples_split=2, verbose=1)
    #Entrenamos modelo y elaboramos predicciones
    model.fit(X, y)
    prediccion=model.predict([[mes,temp,rh,viento,lluvia]])
    st.markdown('cantidad de hectáreas quemada: {}'.format(str(prediccion[0])))
    
#------------------------------
    st.title('')
   
    st.markdown("<h4 style='text-align: center; background-color: orange; opacity:0.8'><center>IPREDICCION NÚMERO INCENDIOS ANUAL </center></h4>", unsafe_allow_html=True)
    st.title('')
    
    forecast = pd.read_csv('data/forecast.csv')
    df_long = pd.melt(forecast, id_vars=['ds'], value_vars=['y', 'yhat1'], var_name='serie', value_name='valor')
    fig = px.line(df_long, x='ds', y='valor', color='serie', title='Serie vs predicción por años en europa',template='plotly_dark',width=1000, height=500)
    fig.update_traces(name='Serie original', selector=dict(name='y'))
    fig.update_traces(name='Estimación', selector=dict(name='yhat1'))
    fig.update_xaxes(title='Años')
    fig.update_yaxes(title='nº de incendios')
    st.plotly_chart(fig,use_container_width=True)
