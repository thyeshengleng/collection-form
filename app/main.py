import streamlit as st
from components.form import render_create_form
from components.table import render_records_table
from components.edit_form import render_edit_form

# Initialize app configuration
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

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'selected_record' not in st.session_state:
    st.session_state.selected_record = None
if 'show_success_message' not in st.session_state:
    st.session_state.show_success_message = False

# Main title
st.title("Collection Action List")

# CRUD Mode Selection
crud_mode = st.radio(
    "Select Operation",
    ["Create New Record", "View/Edit Records"],
    horizontal=True
)

if crud_mode == "Create New Record":
    render_create_form()
else:
    df, edited_df = render_records_table()
    if df is not None and edited_df is not None:
        # Handle edit/delete operations
        selected_rows = edited_df[edited_df["Select"] == True]
        if not selected_rows.empty:
            handle_selected_rows(selected_rows, df) 