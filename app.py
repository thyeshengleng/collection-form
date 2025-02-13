import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
import requests

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
                if st.button("🗑️ Delete Selected", use_container_width=True):
                    if len(selected_rows) > 0:
                        confirm = st.button("⚠️ Confirm Delete")
                        if confirm:
                            for idx in selected_rows.index:
                                df = delete_record(idx)
                            st.success(f"Deleted {len(selected_rows)} record(s)")
                            time.sleep(1)
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
            
            # Rest of your edit form code...
            # (All the fields and save/cancel buttons)

# Show success message if set
if st.session_state.show_success_message:
    st.success("✅ Record updated successfully!")
    # Reset the success message flag
    st.session_state.show_success_message = False

# Add some padding at the bottom
st.write("")
st.write("")