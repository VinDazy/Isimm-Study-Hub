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
#CLIENT_SECRET_FILE='.streamlit/credentials.json'
CLIENT_SECRET_FILE=json.loads(st.secrets["client_secrets_file"])
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']
#OLD_FOLDER_ID="1DFwSgOYhRCXzfbgCTAnT3g_UMMCFqPml"
FOLDER_ID_S1="1S6ezxU7F2bPP-wIvpFpn0sQOTZHx8pxC"
FOLDER_ID_S2="1pAeirUeTlMT-xSe6MpY0oZAuF22CReX8"
FOLDER_ID_L3_S1="1YCwGc0Y7HEpkWzvcqZQthYTqFXbooo5h"
FOLDER_ID_L3_S2="1ANl2WIkAZT46hvU2p0P-XDk9kjecMOF5"

# Generalized cached function
# Generalized cached function for fetching links
@st.cache_data
def get_files_links(folder_id):
    return get_subfiles_link(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, folder_id)

# Fetch the cached data
folder_links_dict_s1 = get_files_links(FOLDER_ID_S1)
folder_links_dict_s2 = get_files_links(FOLDER_ID_S2)
folder_links_dict_l3_s1 = get_files_links(FOLDER_ID_L3_S1)
folder_links_dict_l3_s2 = get_files_links(FOLDER_ID_L3_S2)

with st.sidebar:

    
    # Radio buttons for selecting year
    year = st.radio(
        label="Choose Year : ", 
        options=["L3", "L2"], 
        index=0  # Default to L3 (first option)
    )
    
    # Display semester options based on the selected year
    if year == "L3":
        semester = st.radio(
            label="Choose Semester :", 
            options=["Semester 1", "PFE Material"], 
            index=0  # Default to Semester 1 (first option)
        )
    else:
        semester = st.radio(
            label="Choose Semester : ", 
            options=["Semester 1", "Semester 2"]
        )
    


if year == "L2":
    if semester == "Semester 1":
            display_files_links(folder_links_dict_s1)  # Display links for L2 Semester 1
    else:
            display_files_links(folder_links_dict_s2)  # Display links for L2 Semester 2
else:
            if semester =="Semester 1":
                display_files_links(folder_links_dict_l3_s1)  # Display links for L3 Semester 1
            else:
                display_files_links(folder_links_dict_l3_s2)  # Display links for L3 Semester 2



st.markdown("---")


col1,col2,col3,col4,col5=st.columns(5)
return_home=col3.button("🏠Return Home")
if return_home:
    switch_page("home")
