import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
st.set_page_config(page_title='ISIMM Study Hub',
                   page_icon='media/isimm logo/isimm logo.jpg', layout='wide')
hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            </style>
            """
#!To hide hamburger menu add " #MainMenu {visibility: hidden;} " to the <style>
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
img, bg = st.columns([0.2, 0.8], gap="large")
img.image("media/isimm logo/isimm logo _ 20.png", width=270)
bg.image("media/banner.jpeg", use_column_width=True)
st.markdown("----")
#quote_column,announcement_column=st.columns(2)
st.subheader("🔔 Quote of the day 🔔 ")
@st.cache_data
def Scrape_Quote():
    return scrape_quote()
quote=Scrape_Quote()
#!This is for caching the quote so it won't change when switching between pages
@st.cache_data
def Scrape_Announcement():
    return scrape_announcement()
announcements_dict=Scrape_Announcement()
#!This is for caching the announcements so it won't load again when switching between pages
quote_container = st.empty()
with quote_container:
    st.markdown(
        f'<div style="border: 1px solid rgba(49, 51, 63, 1); border-radius: 0.6rem; padding: 1em;">'
        f'{quote["quote"]} - {quote["author"]}'
        '</div>',
        unsafe_allow_html=True,
        )
st.markdown("----")
st.subheader("📢 Announcements 📢")

# Number of announcements per row
announcements_per_row = 4
num_announcements = len(announcements_dict)
num_rows = -(-num_announcements // announcements_per_row)

for i in range(num_rows):
    columns = st.columns(announcements_per_row)
    start = i * announcements_per_row
    end = min((i + 1) * announcements_per_row, num_announcements)
    
    for j, announcement_idx in enumerate(range(start, end)):
        announcement = announcements_dict[announcement_idx]
        with columns[j]:
            st.markdown(
                f"<div style='border: 1px solid rgba(49, 51, 63, 0.9); border-radius: 0.5rem; padding: 1em; margin: 0.5em;'>"
                f"<b>Title:</b> {announcement['announcement_title']}<br>"
                f"<b>Date:</b> {announcement['announcement_date']}<br>"
                f"<img src='{announcement['announcement_image']}' alt='Announcement Image' style='width: 200px; height: 150px;'><br>"
                f"<b></b> <a href='{announcement['announcement_link']}'>Visit Announcement</a> 📢<br>"
                "</div>",
                unsafe_allow_html=True
            )


st.markdown("---")
subjectResources, schedule, subject_info = st.columns(3)

# Container for Subject Resources
with subjectResources:
    st.image("media/menu/info.png")
    resources_button = st.button("Check Course Materials",use_container_width=True)
    if resources_button:
        switch_page("subjects")

# Container for Schedule
with schedule:
    st.image("media/menu/sched.png")
    schedule_button = st.button("Check Time Table",use_container_width=True)
    if schedule_button:
        switch_page("time tables")

# Container for Subject Information
with subject_info:
    st.image("media/menu/resources.png")
    subject_info_button = st.button("Check useful information", use_container_width=True)
    if subject_info_button:
        switch_page("useful resources")


