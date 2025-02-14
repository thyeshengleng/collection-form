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
    
    # Initialize session state
    if 'server_name' not in st.session_state:
        st.session_state.server_name = ""
    if 'database_name' not in st.session_state:
        st.session_state.database_name = ""
    
    # Help text and examples
    st.markdown("### Server Name")
    st.caption("Try these server names:")
    st.code(".")  # Local default instance
    st.code(".\\SQLEXPRESS")  # Local SQL Express
    st.code("localhost")  # Local default instance
    st.code("localhost\\SQLEXPRESS")  # Local SQL Express
    st.code("(local)")  # Local default instance
    st.code("(local)\\SQLEXPRESS")  # Local SQL Express
    
    # Add a server name selector
    server_options = [
        ".",
        ".\\SQLEXPRESS",
        "localhost",
        "localhost\\SQLEXPRESS",
        "(local)",
        "(local)\\SQLEXPRESS"
    ]
    server_name = st.selectbox(
        "Select or Enter Server Name",
        options=server_options,
        index=None,
        placeholder="Choose a server name or type your own",
        value=st.session_state.server_name
    )
    
    # Database name input
    st.markdown("### Database Name")
    database_name = st.text_input(
        "Enter Database Name",
        value=st.session_state.database_name,
        placeholder="e.g., AED_AssignmentOne",
        help="The name of your database"
    )
    
    # View Data button
    if st.button("View Database Data", use_container_width=True):
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
            
            # Try to connect and fetch data
            conn = pyodbc.connect(conn_str)
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
            
            # Save connection info to session state
            st.session_state.server_name = server_name
            st.session_state.database_name = database_name
            
            # Display data in an interactive table
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
            Common solutions:
            1. Check if SQL Server is running
            2. Verify server name is correct
            3. Make sure database exists
            4. Enable TCP/IP in SQL Server Configuration Manager
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