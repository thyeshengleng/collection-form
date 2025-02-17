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
            # Use CSV for cloud deployment
            is_cloud = st.secrets.get("is_streamlit_cloud", False)
            
            if is_cloud:
                # Load from CSV
                df = pd.read_csv("collection_records.csv")
                st.success("✅ Data loaded from CSV!")
            else:
                # Local database connection
                params = urllib.parse.quote_plus(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=DESKTOP-RMNV9QV\\A2006;'
                    'DATABASE=AED_AssignmentOne;'
                    'UID=sa;'
                    'PWD=oCt2005-ShenZhou6_A2006;'
                    'Trusted_Connection=no;'
                )
                
                engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
                
                with engine.connect() as conn:
                    query = """SELECT TOP 1000 * FROM Debtor ORDER BY CompanyName"""
                    df = pd.read_sql(query, conn)
                    
                    # Save to CSV for cloud deployment
                    df.to_csv("collection_records.csv", index=False)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.error("""
            Please check:
            1. SQL Server instance name is correct (A2006)
            2. SQL Server service is running
            3. SQL Server Browser service is running
            4. Windows Authentication is enabled
            5. TCP/IP protocol is enabled
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