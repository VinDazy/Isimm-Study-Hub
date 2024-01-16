import streamlit as st
from functions import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='ISIMM Study Hub',
                   page_icon='media/isimm logo/isimm logo.jpg', layout='wide')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


st.markdown(hide_streamlit_style, unsafe_allow_html=True)
img, bg = st.columns([0.2, 0.8], gap="large")
img.image("media/isimm logo/isimm logo _ 20.png", width=270)
bg.image("media/banner.jpeg", use_column_width=True)   
CLIENT_SECRET_FILE='.streamlit/credentials.json'
#CLIENT_SECRET_FILE=json.loads(st.secrets["client_secrets_file"])
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']
#OLD_FOLDER_ID="1DFwSgOYhRCXzfbgCTAnT3g_UMMCFqPml"
FOLDER_ID_S1="1S6ezxU7F2bPP-wIvpFpn0sQOTZHx8pxC"
FOLDER_ID_S2="1pAeirUeTlMT-xSe6MpY0oZAuF22CReX8"

@st.cache_data
def get_files_links_s1():
    return get_subfiles_link(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, FOLDER_ID_S1)

@st.cache_data
def get_files_links_s2():
    return get_subfiles_link(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, FOLDER_ID_S2)

with st.sidebar:
    semester=st.selectbox(label="Chose a Semester" ,options=["Semester 2","Semester 1"])

folder_links_dict_s1 = get_subfiles_link(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, FOLDER_ID_S1)
folder_links_dict_s2= get_subfiles_link(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, FOLDER_ID_S2)
if semester=="Semester 1":
    display_files_links(folder_links_dict_s1)
elif semester=="Semester 2":
    display_files_links(folder_links_dict_s2)

st.markdown("---")


col1,col2,col3,col4,col5=st.columns(5)
return_home=col3.button("🏠Return Home")
if return_home:
    switch_page("home")
