import streamlit as st
from datetime import datetime
from app.utils.database import update_record
from app.config.settings import PLUGIN_OPTIONS, REPORT_OPTIONS, STATUS_OPTIONS

def render_edit_form(record, index):
    st.subheader(f"Edit Record: {record['Company Name']}")
    
    # User Type
    user_type = st.radio(
        "User Type *",
        ["New User", "Existing User"],
        index=0 if record["User Type"] == "New User" else 1
    )
    
    # Rest of your edit form code... 