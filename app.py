import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
import requests
import pyodbc

st.set_page_config(page_title="Collection Action List", layout="centered")

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

# Initialize session state for database connection
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False
if 'conn_str' not in st.session_state:
    st.session_state.conn_str = None

# Your Cloudflare Worker URL
WORKER_URL = "https://collection-form.lengthyesheng0721.workers.dev"

# Function to load records from Cloudflare KV
def load_records():
    try:
        response = requests.get(f"{WORKER_URL}/api/form")
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data) if data else pd.DataFrame()
    except:
        return pd.DataFrame()

# Function to save records to Cloudflare KV
def save_records(df):
    try:
        records = df.to_dict('records')
        requests.post(f"{WORKER_URL}/api/form", json=records)
    except:
        st.error("Failed to save data")

# CRUD Operations
def create_record(form_data):
    df = load_records()
    # Convert all values to string before creating new record
    form_data = {k: str(v) for k, v in form_data.items()}
    new_df = pd.DataFrame([form_data])
    df = pd.concat([df, new_df], ignore_index=True)
    save_records(df)
    return df

def update_record(index, form_data):
    df = load_records()
    # Convert all values to string before updating
    form_data = {k: str(v) for k, v in form_data.items()}
    for key, value in form_data.items():
        df.at[index, key] = value
    save_records(df)
    return df

def delete_record(index):
    df = load_records()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_records(df)
    return df

# Main title
st.title("Collection Action List")

# CRUD Mode Selection
crud_mode = st.radio(
    "Select Operation",
    ["Create New Record", "View/Edit Records"],
    horizontal=True
)

if crud_mode == "Create New Record":
    st.session_state.edit_mode = False
    st.session_state.selected_record = None
    
    # User Type Selection in a single column
    st.subheader("User Type")
    new_user = st.checkbox("New User")
    existing_user = st.checkbox("Existing User")

    if st.session_state.form_submitted and not (new_user or existing_user):
        st.error("Please select a user type")

    # Create form fields
    st.subheader("Company Information")
    company_name = st.text_input("COMPANY NAME", value="")
    if st.session_state.form_submitted and not company_name:
        st.error("Company name is required")

    email = st.text_input("EMAIL", value="")
    if st.session_state.form_submitted and not email:
        st.error("Email is required")
    elif st.session_state.form_submitted and '@' not in email:
        st.error("Please enter a valid email address")

    address = st.text_area("ADDRESS", value="")
    if st.session_state.form_submitted and not address:
        st.error("Address is required")

    business_info = st.text_input("BUSINESS INFO", value="")
    if st.session_state.form_submitted and not business_info:
        st.error("Business info is required")

    tax_id = st.text_input("TAX ID", value="")
    if st.session_state.form_submitted and not tax_id:
        st.error("Tax ID is required")

    e_invoice_start_date = st.date_input("E-INVOICE START DATE", value=None)
    if st.session_state.form_submitted and not e_invoice_start_date:
        st.error("E-Invoice start date is required")

    # Checkboxes for Plug in Module
    st.subheader("PLUG IN MODULE")
    plugin_options = [
        "Deposit Plugin",
        "Fix Asset Plugin",
        "Shipment Plugin",
        "Stock Request Plugin",
        "Doc Control Plugin"
    ]

    # Display plugins in a single column for mobile
    selected_plugins = []
    for plugin in plugin_options:
        if st.checkbox(plugin):
            selected_plugins.append(plugin)

    if st.session_state.form_submitted and not selected_plugins:
        st.error("Please select at least one plugin")

    st.subheader("Additional Information")
    vpn_info = st.text_input("VPN INFO", value="")
    if st.session_state.form_submitted and not vpn_info:
        st.error("VPN info is required")

    module_license = st.text_input("MODULE & USER LICENSE", value="")
    if st.session_state.form_submitted and not module_license:
        st.error("Module & User License is required")

    # Report Design Template section with checkboxes
    st.subheader("Reports")
    st.markdown("### REPORT DESIGN TEMPLATE *")
    report_options = ["SO", "DO", "INV", "PO", "PICKING LIST"]
    selected_reports = []
    
    # Create two columns for report options
    report_cols = st.columns(2)
    for idx, report in enumerate(report_options):
        with report_cols[idx % 2]:
            if st.checkbox(report, key=f"report_{report}"):
                selected_reports.append(report)
    
    if st.session_state.form_submitted and not selected_reports:
        st.error("⚠️ Please select at least one report template!")

    migration_master = st.text_input("MIGRATION MASTER DATA", value="")
    migration_outstanding = st.text_input("MIGRATION (OUTSTANDING BALANCE)", value="")

    st.subheader("Status")
    status = st.selectbox("Status", ["", "pending", "complete", "AR/Ap, Stock pending"])
    if st.session_state.form_submitted and not status:
        st.error("Status is required")

    # Add some spacing
    st.write("")
    st.write("")

    if st.button("Save Record", use_container_width=True):
        st.session_state.form_submitted = True
        
        # Validate all required fields
        is_valid = all([
            new_user or existing_user,
            company_name,
            email and '@' in email,
            address,
            business_info,
            tax_id,
            e_invoice_start_date,
            selected_plugins,
            vpn_info,
            module_license,
            selected_reports,
            migration_master,
            migration_outstanding,
            status
        ])
        
        if is_valid:
            # Create a dictionary of all the form data
            form_data = {
                "User Type": "New User" if new_user else "Existing User" if existing_user else "",
                "Company Name": company_name,
                "Email": email,
                "Address": address,
                "Business Info": business_info,
                "Tax ID": tax_id,
                "E-Invoice Start Date": e_invoice_start_date.strftime("%Y-%m-%d") if e_invoice_start_date else "",
                "Plug In Module": ", ".join(selected_plugins) if selected_plugins else "",
                "VPN Info": vpn_info,
                "Module & User License": module_license,
                "Report Design Template": ", ".join(selected_reports) if selected_reports else "",
                "Migration Master Data": migration_master,
                "Migration Outstanding Balance": migration_outstanding,
                "Status": status
            }
            
            df = create_record(form_data)
            st.success("✅ Record saved successfully!")
            st.write(df.tail(1))
        else:
            st.error("Please fill in all required fields correctly")

else:  # View/Edit Records
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
        
        # Create a view DataFrame
        view_df = df[[
            "Company Name", 
            "User Type", 
            "Email", 
            "Status"
        ]].copy()
        
        # Display selectable table
        selected = st.data_editor(
            view_df,
            hide_index=False,
            use_container_width=True,
            column_config={
                "Company Name": st.column_config.TextColumn("Company Name", width="medium"),
                "User Type": st.column_config.TextColumn("User Type", width="small"),
                "Email": st.column_config.TextColumn("Email", width="medium"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    width="small",
                    options=["pending", "complete", "AR/Ap, Stock pending"]
                ),
            },
            disabled=view_df.columns.tolist(),  # Make all columns read-only
            key="data_editor"
        )

        # Get selected index from the selection
        if "edited_rows" in st.session_state["data_editor"]:
            edited_rows = st.session_state["data_editor"]["edited_rows"]
            if edited_rows:
                selected_index = list(edited_rows.keys())[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", use_container_width=True):
                        st.session_state.edit_mode = True
                        st.session_state.selected_record = selected_index
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Delete", use_container_width=True):
                        confirm = st.button("⚠️ Confirm Delete")
                        if confirm:
                            df = delete_record(selected_index)
                            st.success("Record deleted successfully!")
                            time.sleep(1)
                            st.rerun()

# Show success message if set
if st.session_state.show_success_message:
    st.success("✅ Record updated successfully!")
    # Reset the success message flag
    st.session_state.show_success_message = False

# Add some padding at the bottom
st.write("")
st.write("")

def connect_to_database(server, database, trusted=True, username=None, password=None):
    try:
        if trusted:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        else:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        conn = pyodbc.connect(conn_str)
        st.session_state.conn_str = conn_str
        return conn
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def get_tables(conn):
    try:
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        """
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error getting tables: {str(e)}")
        return pd.DataFrame()

def get_table_data(conn, table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error getting table data: {str(e)}")
        return pd.DataFrame()

# Main app
st.title("SQL Server Database Viewer")

# Database connection section
with st.sidebar:
    st.header("Database Connection")
    server_name = st.text_input("Server Name", "localhost")
    database_name = st.text_input("Database Name")
    
    auth_type = st.radio("Authentication", ["Windows Authentication", "SQL Server Authentication"])
    
    if auth_type == "SQL Server Authentication":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Connect"):
            conn = connect_to_database(server_name, database_name, False, username, password)
            if conn:
                st.session_state.db_connected = True
                st.success("Connected successfully!")
                conn.close()
    else:
        if st.button("Connect"):
            conn = connect_to_database(server_name, database_name)
            if conn:
                st.session_state.db_connected = True
                st.success("Connected successfully!")
                conn.close()

# Main content
if st.session_state.db_connected and st.session_state.conn_str:
    try:
        conn = pyodbc.connect(st.session_state.conn_str)
        
        # Get and display tables
        tables_df = get_tables(conn)
        if not tables_df.empty:
            selected_table = st.selectbox("Select Table", tables_df['TABLE_NAME'].tolist())
            
            if selected_table:
                # Get and display table data
                data = get_table_data(conn, selected_table)
                if not data.empty:
                    st.subheader(f"Table: {selected_table}")
                    
                    # Add search functionality
                    search_term = st.text_input("Search in table", "")
                    if search_term:
                        # Search across all columns
                        mask = data.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
                        data = data[mask]
                    
                    # Display table with options
                    st.dataframe(
                        data,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Export options
                    if st.button("Export to CSV"):
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.db_connected = False

# Disconnect button
if st.session_state.db_connected:
    if st.sidebar.button("Disconnect"):
        st.session_state.db_connected = False
        st.session_state.conn_str = None
        st.rerun()