import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import os
import time
import requests

# Initialize session state for database connection
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False
if 'server_name' not in st.session_state:
    st.session_state.server_name = ""
if 'database_name' not in st.session_state:
    st.session_state.database_name = ""

# Initialize session state
if 'view_database' not in st.session_state:
    st.session_state.view_database = False

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

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'selected_record' not in st.session_state:
    st.session_state.selected_record = None

# Initialize session state for success message
if 'show_success_message' not in st.session_state:
    st.session_state.show_success_message = False

# Your Cloudflare Worker URL
WORKER_URL = "https://collection-form.southlinks.workers.dev"

# Database connection function
def connect_to_db(server, database):
    try:
        # Clean up server name to handle backslashes
        server = server.replace('\\', '\\\\')
        
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
            'TrustServerCertificate=yes;'
        )
        
        # Print connection string for debugging
        print(f"Connection string: {conn_str}")
        
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        # Print available drivers for debugging
        print("Available drivers:", [x for x in pyodbc.drivers()])
        return None

# Function to load records from SQL
def load_records():
    try:
        conn = connect_to_db(st.session_state.server_name, st.session_state.database_name)
        if conn:
            query = "SELECT * FROM CollectionActionList"  # Replace with your table name
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading records: {str(e)}")
        return pd.DataFrame()

# Function to save record to SQL
def save_record(form_data):
    try:
        conn = connect_to_db(st.session_state.server_name, st.session_state.database_name)
        if conn:
            cursor = conn.cursor()
            
            # Insert query
            query = """
            INSERT INTO CollectionActionList (
                UserType, CompanyName, Email, Address, BusinessInfo,
                TaxID, EInvoiceStartDate, PlugInModule, VPNInfo,
                ModuleLicense, ReportTemplate, MigrationMasterData,
                MigrationOutstandingBalance, Status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Convert form_data to tuple for SQL insert
            values = (
                form_data['User Type'],
                form_data['Company Name'],
                form_data['Email'],
                form_data['Address'],
                form_data['Business Info'],
                form_data['Tax ID'],
                form_data['E-Invoice Start Date'],
                form_data['Plug In Module'],
                form_data['VPN Info'],
                form_data['Module & User License'],
                form_data['Report Design Template'],
                form_data['Migration Master Data'],
                form_data['Migration Outstanding Balance'],
                form_data['Status']
            )
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        st.error(f"Error saving record: {str(e)}")
        return False

# Function to update record in SQL
def update_record(record_id, form_data):
    try:
        conn = connect_to_db(st.session_state.server_name, st.session_state.database_name)
        if conn:
            cursor = conn.cursor()
            
            # Update query
            query = """
            UPDATE CollectionActionList
            SET UserType = ?,
                CompanyName = ?,
                Email = ?,
                Address = ?,
                BusinessInfo = ?,
                TaxID = ?,
                EInvoiceStartDate = ?,
                PlugInModule = ?,
                VPNInfo = ?,
                ModuleLicense = ?,
                ReportTemplate = ?,
                MigrationMasterData = ?,
                MigrationOutstandingBalance = ?,
                Status = ?
            WHERE ID = ?
            """
            
            values = (
                form_data['User Type'],
                form_data['Company Name'],
                form_data['Email'],
                form_data['Address'],
                form_data['Business Info'],
                form_data['Tax ID'],
                form_data['E-Invoice Start Date'],
                form_data['Plug In Module'],
                form_data['VPN Info'],
                form_data['Module & User License'],
                form_data['Report Design Template'],
                form_data['Migration Master Data'],
                form_data['Migration Outstanding Balance'],
                form_data['Status'],
                record_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        st.error(f"Error updating record: {str(e)}")
        return False

# Function to delete record from SQL
def delete_record(record_id):
    try:
        conn = connect_to_db(st.session_state.server_name, st.session_state.database_name)
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CollectionActionList WHERE ID = ?", record_id)
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        st.error(f"Error deleting record: {str(e)}")
        return False

# Create SQL table if it doesn't exist
def create_table():
    try:
        conn = connect_to_db(st.session_state.server_name, st.session_state.database_name)
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CollectionActionList' AND xtype='U')
                CREATE TABLE CollectionActionList (
                    ID INT IDENTITY(1,1) PRIMARY KEY,
                    UserType NVARCHAR(50),
                    CompanyName NVARCHAR(200),
                    Email NVARCHAR(200),
                    Address NVARCHAR(MAX),
                    BusinessInfo NVARCHAR(MAX),
                    TaxID NVARCHAR(100),
                    EInvoiceStartDate DATE,
                    PlugInModule NVARCHAR(MAX),
                    VPNInfo NVARCHAR(MAX),
                    ModuleLicense NVARCHAR(MAX),
                    ReportTemplate NVARCHAR(MAX),
                    MigrationMasterData NVARCHAR(MAX),
                    MigrationOutstandingBalance NVARCHAR(MAX),
                    Status NVARCHAR(50),
                    CreatedDate DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        st.error(f"Error creating table: {str(e)}")
        return False

# Create table when app starts
create_table()

# Main title
st.title("Collection Action List")

# Main navigation
page = st.radio("Select Page", ["Collection Form", "View Database"], horizontal=True)

if page == "Collection Form":
    # Your existing collection form code here
    # (CSV-based collection form without SQL connection)
    
    # File path for data storage
    DATA_FILE = "collection_records.csv"

    # Function to load existing records
    def load_records():
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)
        return pd.DataFrame()

    # Function to save records
    def save_records(df):
        df.to_csv(DATA_FILE, index=False)

    # CRUD Operations
    def create_record(form_data):
        df = load_records()
        new_df = pd.DataFrame([form_data])
        df = pd.concat([df, new_df], ignore_index=True)
        save_records(df)
        return df

    # CRUD Mode Selection
    crud_mode = st.radio(
        "Select Operation",
        ["Create New Record", "View/Edit Records"],
        horizontal=True
    )

    # Database Connection Form
    if not st.session_state.db_connected:
        st.title("Database Connection")
        
        # Show available drivers
        st.write("Available SQL Server Drivers:")
        st.write([x for x in pyodbc.drivers() if 'SQL Server' in x])
        
        with st.form("db_connection"):
            server_name = st.text_input(
                "Server Name", 
                value="DESKTOP-RMNV9QV\\A2006",
                help="Example: DESKTOP-RMNV9QV\\A2006 or localhost\\SQLEXPRESS"
            )
            database_name = st.text_input(
                "Database Name", 
                value="AED_AssignmentOne",
                help="Example: AED_AssignmentOne"
            )
            
            # Add driver selection
            drivers = [x for x in pyodbc.drivers() if 'SQL Server' in x]
            selected_driver = st.selectbox("Select SQL Server Driver", drivers)
            
            col1, col2 = st.columns(2)
            with col1:
                connect_button = st.form_submit_button("Connect", use_container_width=True)
            
            if connect_button:
                conn = connect_to_db(server_name, database_name)
                if conn:
                    st.session_state.db_connected = True
                    st.session_state.server_name = server_name
                    st.session_state.database_name = database_name
                    st.success("✅ Connected to database successfully!")
                    st.rerun()
                conn.close()

    # Main Application (only show if connected to database)
    if st.session_state.db_connected:
        st.title("Collection Action List")
        
        # Add disconnect button in sidebar
        with st.sidebar:
            st.write(f"Connected to: {st.session_state.database_name}")
            if st.button("Disconnect", use_container_width=True):
                st.session_state.db_connected = False
                st.session_state.server_name = ""
                st.session_state.database_name = ""
                st.rerun()
        
        # Load and display existing records
        df = load_records()
        
        if not df.empty:
            st.subheader("Search Records")
            search_term = st.text_input("Search by Company Name or Email", "")
            
            if search_term:
                df = df[
                    df["Company Name"].str.contains(search_term, case=False, na=False) |
                    df["Email"].str.contains(search_term, case=False, na=False)
                ]
            
            st.subheader("Existing Records")
            
            # Create a view DataFrame with selection column
            view_df = df.copy()
            view_df.insert(0, "Select", False)
            
            # Display interactive table
            edited_df = st.data_editor(
                view_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        help="Select to edit or delete",
                        default=False,
                        width="small"
                    ),
                    "Company Name": st.column_config.TextColumn("Company Name", width="medium"),
                    "User Type": st.column_config.TextColumn("User Type", width="small"),
                    "Email": st.column_config.TextColumn("Email", width="medium"),
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        width="small",
                        options=["pending", "complete", "AR/Ap, Stock pending"]
                    ),
                },
                disabled=["Company Name", "User Type", "Email", "Status"],
                key="data_editor"
            )
            
            # Get selected rows
            selected_rows = edited_df[edited_df["Select"] == True]
            
            # Show action buttons if any rows are selected
            if not selected_rows.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit Selected", use_container_width=True):
                        if len(selected_rows) == 1:
                            idx = selected_rows.index[0]
                            st.session_state.edit_mode = True
                            st.session_state.selected_record = idx
                            st.rerun()
                        else:
                            st.warning("Please select only one record to edit")
                
                with col2:
                    # Initialize delete confirmation state
                    if 'delete_confirmation' not in st.session_state:
                        st.session_state.delete_confirmation = False
                    
                    # Show delete button
                    if not st.session_state.delete_confirmation:
                        if st.button("🗑️ Delete Selected", use_container_width=True):
                            st.session_state.delete_confirmation = True
                            st.rerun()
                    
                    # Show confirmation button
                    if st.session_state.delete_confirmation:
                        col3, col4 = st.columns(2)
                        with col3:
                            if st.button("⚠️ Confirm", use_container_width=True):
                                for idx in selected_rows.index:
                                    delete_record(idx)
                                st.success(f"Deleted {len(selected_rows)} record(s)")
                                st.session_state.delete_confirmation = False
                                time.sleep(1)
                                st.rerun()
                        with col4:
                            if st.button("Cancel", use_container_width=True):
                                st.session_state.delete_confirmation = False
                                st.rerun()

            # Edit form
            if st.session_state.edit_mode and st.session_state.selected_record is not None:
                record = df.iloc[st.session_state.selected_record]
                
                st.subheader(f"Edit Record: {record['Company Name']}")
                
                # User Type
                user_type = st.radio(
                    "User Type *",
                    ["New User", "Existing User"],
                    index=0 if record["User Type"] == "New User" else 1
                )
                
                # Company Information
                company_name = st.text_input("COMPANY NAME *", value=record["Company Name"])
                email = st.text_input("EMAIL *", value=record["Email"])
                address = st.text_area("ADDRESS *", value=record["Address"])
                business_info = st.text_input("BUSINESS INFO *", value=record["Business Info"])
                tax_id = st.text_input("TAX ID *", value=record["Tax ID"])
                
                # E-Invoice Start Date
                try:
                    default_date = datetime.strptime(record["E-Invoice Start Date"], "%Y-%m-%d").date()
                except:
                    default_date = datetime.now().date()
                e_invoice_start_date = st.date_input("E-INVOICE START DATE *", value=default_date)
                
                # Plug in Module
                st.subheader("PLUG IN MODULE *")
                plugin_options = [
                    "Deposit Plugin",
                    "Fix Asset Plugin",
                    "Shipment Plugin",
                    "Stock Request Plugin",
                    "Doc Control Plugin"
                ]
                existing_plugins = record["Plug In Module"].split(", ") if record["Plug In Module"] else []
                selected_plugins = []
                for plugin in plugin_options:
                    if st.checkbox(plugin, key=f"edit_plugin_{plugin}", value=plugin in existing_plugins):
                        selected_plugins.append(plugin)
                
                # Additional Information
                vpn_info = st.text_input("VPN INFO *", value=record["VPN Info"])
                module_license = st.text_input("MODULE & USER LICENSE *", value=record["Module & User License"])
                
                # Report Design Template
                st.markdown("### REPORT DESIGN TEMPLATE *")
                report_options = ["SO", "DO", "INV", "PO", "PICKING LIST"]
                existing_reports = record["Report Design Template"].split(", ") if record["Report Design Template"] else []
                selected_reports = []
                report_cols = st.columns(2)
                for idx, report in enumerate(report_options):
                    with report_cols[idx % 2]:
                        if st.checkbox(report, key=f"edit_report_{report}", value=report in existing_reports):
                            selected_reports.append(report)
                
                # Migration Information
                migration_master = st.text_input("MIGRATION MASTER DATA *", value=record["Migration Master Data"])
                migration_outstanding = st.text_input("MIGRATION (OUTSTANDING BALANCE) *", value=record["Migration Outstanding Balance"])
                
                # Status
                status = st.selectbox(
                    "Status *",
                    ["pending", "complete", "AR/Ap, Stock pending"],
                    index=["pending", "complete", "AR/Ap, Stock pending"].index(record["Status"])
                )
                
                # Save/Cancel buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Changes", use_container_width=True):
                        updated_data = {
                            "User Type": user_type,
                            "Company Name": company_name,
                            "Email": email,
                            "Address": address,
                            "Business Info": business_info,
                            "Tax ID": tax_id,
                            "E-Invoice Start Date": e_invoice_start_date.strftime("%Y-%m-%d"),
                            "Plug In Module": ", ".join(selected_plugins),
                            "VPN Info": vpn_info,
                            "Module & User License": module_license,
                            "Report Design Template": ", ".join(selected_reports),
                            "Migration Master Data": migration_master,
                            "Migration Outstanding Balance": migration_outstanding,
                            "Status": status
                        }
                        update_record(st.session_state.selected_record, updated_data)
                        st.success(f"✅ Record for {company_name} updated successfully!")
                        time.sleep(1)
                        st.session_state.edit_mode = False
                        st.session_state.selected_record = None
                        st.rerun()
                
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.edit_mode = False
                        st.session_state.selected_record = None
                        st.rerun()

    # Show success message if set
    if st.session_state.show_success_message:
        st.success("✅ Record updated successfully!")
        # Reset the success message flag
        st.session_state.show_success_message = False

    # Add some padding at the bottom
    st.write("")
    st.write("")

elif page == "View Database":
    st.subheader("Database Connection")
    
    with st.form("db_connection"):
        server_name = st.text_input(
            "Server Name", 
            value="DESKTOP-RMNV9QV\\A2006",
            help="Example: DESKTOP-RMNV9QV\\A2006"
        )
        database_name = st.text_input(
            "Database Name", 
            value="AED_AssignmentOne",
            help="Example: AED_AssignmentOne"
        )
        
        if st.form_submit_button("Connect"):
            st.session_state.view_database = True
            view_sql_data(server_name, database_name)

# Add some padding at the bottom
st.write("")
st.write("")