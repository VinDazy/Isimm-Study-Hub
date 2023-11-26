import streamlit as st
from functions import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='ISIMM Study Hub',
                   page_icon='media\isimm logo\isimm logo.jpg', layout='wide')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


st.markdown(hide_streamlit_style, unsafe_allow_html=True)
img, bg = st.columns([0.2, 0.8], gap="large")
img.image("media\isimm logo\isimm logo _ 20.png", width=270)
bg.image("media\\banner.jpeg", use_column_width=True)
CLIENT_SECRET_FILE='download\client_secrets_file.json'
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']
FOLDER_ID="1DFwSgOYhRCXzfbgCTAnT3g_UMMCFqPml"
@st.cache_data
def get_sub_folderLinks():
    return get_subfolder_links(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, FOLDER_ID)


folder_links_dict = get_sub_folderLinks()

st.markdown("---")


display_subfolder_links(folder_links_dict)

col1,col2,col3,col4,col5=st.columns(5)
return_home=col3.button("🏠Return Home")
if return_home:
    switch_page("home")
