import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
import pyodbc
from sqlalchemy import create_engine
from app.utils.database import load_records, save_records, create_record, update_record, delete_record
from app.components.form import render_create_form
from app.components.table import render_records_table
from app.components.edit_form import render_edit_form
import urllib.parse

def render_db_form():
    st.subheader("Database Connection")
    
    # View Data button
    if st.button("👁️ View Database Data", use_container_width=True):
        try:
            # API endpoint
            api_url = "http://localhost:8001/api/debtor"
            
            # Try to fetch data
            with st.spinner("Fetching data..."):
                response = requests.get(api_url)
                
                if response.status_code == 200:
                    # Convert JSON to DataFrame
                    data = response.json()
                    df = pd.DataFrame(data)
                    
                    # Display data
                    st.success("✅ Data retrieved successfully!")
                    st.dataframe(
                        df,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "CompanyName": st.column_config.TextColumn("Company Name", width="medium"),
                            "RegisterNo": st.column_config.TextColumn("Register No", width="small"),
                            "EmailAddress": st.column_config.TextColumn("Email", width="medium"),
                            "IsActive": st.column_config.CheckboxColumn("Active", width="small"),
                        }
                    )
                else:
                    st.error(f"❌ API Error: {response.text}")
            
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
            st.error("""
            Please check:
            1. API server is running (python api_server.py)
            2. API endpoint is correct
            3. Network connection is working
            4. No firewall blocking port 8001
            """)

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