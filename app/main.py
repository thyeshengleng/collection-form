import streamlit as st
import pandas as pd
from datetime import datetime
import time
from utils.database import load_records, save_records, create_record, update_record, delete_record
from config.settings import WORKER_URL

# Hide Streamlit menu and footer
st.set_page_config(
    page_title="Collection Action List",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide menu button and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Rest of your Streamlit app code... 