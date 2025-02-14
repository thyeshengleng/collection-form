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
    if 'is_connected' not in st.session_state:
        st.session_state.is_connected = False
    
    # Server name input
    server_name = st.text_input(
        "Server Name",
        value=st.session_state.server_name,
        placeholder="Enter server name (e.g., DESKTOP-ABC\\SQLEXPRESS)",
        help="Your SQL Server instance name"
    )
    
    # Database name input
    database_name = st.text_input(
        "Database Name",
        value=st.session_state.database_name,
        placeholder="Enter database name",
        help="The name of your database"
    )
    
    # Connect button
    if st.button("Connect to Database", use_container_width=True):
        try:
            # Clean up server name to handle backslashes
            server = server_name.replace('\\', '\\\\')
            
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database_name};'
                'Trusted_Connection=yes;'
                'TrustServerCertificate=yes;'
            )
            
            # Try to connect
            conn = pyodbc.connect(conn_str)
            conn.close()
            
            # Save connection info to session state
            st.session_state.server_name = server_name
            st.session_state.database_name = database_name
            st.session_state.is_connected = True
            
            st.success("✅ Connected to database successfully!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
            st.session_state.is_connected = False

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
        if st.session_state.is_connected:
            render_create_form()
        else:
            st.warning("Please connect to database first")
            render_db_form()
    else:  # View/Edit Records
        if st.session_state.is_connected:
            df, edited_df = render_records_table()
            if df is not None and edited_df is not None:
                # Handle edit/delete operations
                selected_rows = edited_df[edited_df["Select"] == True]
                if not selected_rows.empty:
                    handle_selected_rows(selected_rows, df)
        else:
            st.warning("Please connect to database first")
            render_db_form()

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