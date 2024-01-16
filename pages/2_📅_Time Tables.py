from streamlit_extras.switch_page_button import switch_page
import streamlit as st
from functions import *
import time
st.set_page_config(page_title='ISIMM Study Hub',page_icon='media/isimm logo/isimm logo.jpg',layout='wide')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

img,bg=st.columns([0.2,0.8],gap="large")

img.image("media/isimm logo/isimm logo _ 20.png", width=270)
bg.image("media/banner.jpeg", use_column_width=True)
with st.sidebar:
    semester=st.selectbox(label="Chose a Semester" ,options=["Semester 2","Semester 1"])
tdGroups=["TD1","TD2","TD3","TD4","TD5"]
group=st.selectbox("Please choose your TD group ",options=tdGroups)
filePath=f"resources/timeTables/{semester}/"+group+".png"
image=st.image(image=filePath,use_column_width=True)
st.toast(f" Displaying {group[:-1]+' '+group[-1]} Time Table",icon="🙌")

col1,col2,col3,col4,col5=st.columns(5)
return_home=col3.button("🏠Return Home")
if return_home:
    switch_page("home") 