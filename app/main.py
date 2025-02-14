import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
import pyodbc
from app.utils.database import load_records, save_records, create_record, update_record, delete_record
from app.components.form import render_create_form
from app.components.table import render_records_table
from app.components.edit_form import render_edit_form

def render_db_form():
    st.subheader("Database Connection")
    
    # Initialize session state for database connection
    if 'server_name' not in st.session_state:
        st.session_state.server_name = ""
    if 'database_name' not in st.session_state:
        st.session_state.database_name = ""
    
    # Help text and examples
    st.markdown("### Server Name")
    st.caption("Common formats:")
    st.code("localhost\\SQLEXPRESS")
    st.code("(local)\\SQLEXPRESS")
    st.code("DESKTOP-ABC\\SQLEXPRESS")
    
    server_name = st.text_input(
        "Enter Server Name",
        value=st.session_state.server_name,
        help="Your SQL Server instance name"
    )
    
    # Database name input
    st.markdown("### Database Name")
    database_name = st.text_input(
        "Enter Database Name",
        value=st.session_state.database_name,
        help="The name of your database"
    )
    
    # Save button
    if st.button("Save Connection Info", use_container_width=True):
        st.session_state.server_name = server_name
        st.session_state.database_name = database_name
        st.success("✅ Connection info saved!")
        time.sleep(1)
        st.rerun()

def main():
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
        ["Database Connection", "Create New Record", "View/Edit Records"],
        horizontal=True
    )

    if crud_mode == "Database Connection":
        render_db_form()
    elif crud_mode == "Create New Record":
        render_create_form()
    else:  # View/Edit Records
        df, edited_df = render_records_table()
        if df is not None and edited_df is not None:
            # Handle edit/delete operations
            selected_rows = edited_df[edited_df["Select"] == True]
            if not selected_rows.empty:
                handle_selected_rows(selected_rows, df)

def handle_selected_rows(selected_rows, df):
    if len(selected_rows) == 1:
        idx = selected_rows.index[0]
        record = df.iloc[idx]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit Selected", use_container_width=True):
                st.session_state.edit_mode = True
                st.session_state.selected_record = idx
                st.rerun()
        
        with col2:
            if st.button("🗑️ Delete Selected", use_container_width=True):
                if st.button("⚠️ Confirm Delete"):
                    df = delete_record(idx)
                    st.success(f"Deleted record for {record['Company Name']}")
                    time.sleep(1)
                    st.rerun()

    # Show edit form if in edit mode
    if st.session_state.edit_mode and st.session_state.selected_record is not None:
        record = df.iloc[st.session_state.selected_record]
        render_edit_form(record, st.session_state.selected_record)

if __name__ == "__main__":
    main() 