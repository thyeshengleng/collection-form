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

def render_db_form():
    st.subheader("Database Connection")
    
    # View Data button
    if st.button("👁️ View Database Data", use_container_width=True):
        try:
            # Create connection string for SQL Server 2006
            conn_str = (
                'DRIVER={SQL Server};'
                'SERVER=DESKTOP-RMNV9QV\\A2006;'  # Use instance name
                'DATABASE=AED_AssignmentOne;'
                'UID=sa;'
                'PWD=oCt2005-ShenZhou6_A2006;'
                'TrustServerCertificate=yes;'
            )
            
            # Try to connect and fetch data
            with st.spinner("Connecting to database..."):
                # First try to connect
                st.info("Attempting to connect to SQL Server...")
                conn = pyodbc.connect(conn_str, timeout=30)
                
                # If connected, fetch data
                st.info("Connected! Fetching data...")
                query = """
                    SELECT TOP 1000 
                        AccNo,
                        CompanyName,
                        RegisterNo,
                        Address1,
                        Address2,
                        Address3,
                        Address4,
                        PostCode,
                        Phone1,
                        Phone2,
                        EmailAddress,
                        WebURL,
                        NatureOfBusiness,
                        IsActive
                    FROM Debtor
                    ORDER BY CompanyName
                """
                df = pd.read_sql(query, conn)
                conn.close()
            
            # Display data
            st.success("✅ Connected successfully! Showing database records:")
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
            
            # Show available SQL Server drivers
            try:
                drivers = pyodbc.drivers()
                st.info("Available SQL Server drivers:")
                for driver in drivers:
                    if 'SQL Server' in driver:
                        st.code(driver)
            except:
                st.warning("Could not list available drivers")

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