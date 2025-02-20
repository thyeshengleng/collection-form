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
            # Create SQLAlchemy connection string
            params = urllib.parse.quote_plus(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-RMNV9QV\\A2006;'
                'DATABASE=AED_AssignmentOne;'
                'UID=sa;'
                'PWD=oCt2005-ShenZhou6_A2006;'
                'Trusted_Connection=no;'
            )
            
            # Create SQLAlchemy engine
            engine = create_engine(
                f"mssql+pyodbc:///?odbc_connect={params}",
                pool_pre_ping=True,  # Check connection before using
                pool_recycle=3600    # Recycle connections after 1 hour
            )
            
            # Try to connect and fetch data
            with st.spinner("Connecting to database..."):
                st.info("Attempting to connect to SQL Server...")
                
                # Test connection first
                with engine.connect() as conn:
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

def render_popup_view(record):
    # Display the form content
    st.subheader(f"View Record: {record.get('Company Name', '')}")
    
    # User Type
    st.markdown("### User Type")
    st.text_input("User Type", value=record.get('User Type', ''), disabled=True)
    
    # Company Information
    st.markdown("### Company Information")
    st.text_input("Company Name", value=record.get('Company Name', ''), disabled=True)
    st.text_input("Email", value=record.get('Email', ''), disabled=True)
    st.text_area("Address", value=record.get('Address', ''), disabled=True)
    st.text_input("Business Info", value=record.get('Business Info', ''), disabled=True)
    st.text_input("Tax ID", value=record.get('Tax ID', ''), disabled=True)
    st.text_input("E-Invoice Start Date", value=record.get('E-Invoice Start Date', ''), disabled=True)
    
    # Plugin Information
    st.markdown("### Plug In Module")
    st.text_area("Selected Plugins", value=record.get('Plug In Module', ''), disabled=True)
    
    # Additional Information
    st.markdown("### Additional Information")
    st.text_input("VPN Info", value=record.get('VPN Info', ''), disabled=True)
    st.text_input("Module & User License", value=record.get('Module & User License', ''), disabled=True)
    
    # Report Information
    st.markdown("### Report Design Template")
    st.text_area("Selected Reports", value=record.get('Report Design Template', ''), disabled=True)
    
    # Migration Information
    st.markdown("### Migration Information")
    st.text_input("Master Data", value=record.get('Migration Master Data', ''), disabled=True)
    st.text_input("Outstanding Balance", value=record.get('Migration Outstanding Balance', ''), disabled=True)
    
    # Status
    st.markdown("### Status")
    st.text_input("Current Status", value=record.get('Status', ''), disabled=True)
    
    # Close button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Close", use_container_width=True):
            st.session_state.view_mode = False
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
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = False
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
            # Handle selected rows
            selected_rows = edited_df[edited_df["Select"] == True]
            if not selected_rows.empty:
                idx = selected_rows.index[0]
                record = df.iloc[idx]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👁️ View Details", use_container_width=True):
                        st.session_state.view_mode = True
                        st.session_state.selected_record = idx
                        st.rerun()
                
                with col2:
                    if st.button("✏️ Edit Selected", use_container_width=True):
                        st.session_state.edit_mode = True
                        st.session_state.selected_record = idx
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete Selected", use_container_width=True):
                        if st.button("⚠️ Confirm Delete"):
                            df = delete_record(idx)
                            st.success(f"Deleted record for {record['Company Name']}")
                            time.sleep(1)
                            st.rerun()

            # Show view form if in view mode
            if st.session_state.view_mode and st.session_state.selected_record is not None:
                record = df.iloc[st.session_state.selected_record]
                render_popup_view(record)

            # Show edit form if in edit mode
            if st.session_state.edit_mode and st.session_state.selected_record is not None:
                record = df.iloc[st.session_state.selected_record]
                render_edit_form(record, st.session_state.selected_record)

if __name__ == "__main__":
    main() 