import streamlit as st
from datetime import datetime
from app.config.settings import PLUGIN_OPTIONS, REPORT_OPTIONS, STATUS_OPTIONS
from app.utils.database import create_record

def handle_form_submit(new_user, existing_user, company_name, email, address,
                      business_info, tax_id, e_invoice_start_date, selected_plugins,
                      vpn_info, module_license, selected_reports, migration_master,
                      migration_outstanding, status):
    # Validate required fields
    if not (new_user or existing_user):
        st.error("Please select a user type")
        return None
    
    if not company_name or not email:
        st.error("Company Name and Email are required")
        return None

    # Create form data dictionary
    form_data = {
        "User Type": "New User" if new_user else "Existing User",
        "Company Name": company_name,
        "Email": email,
        "Address": address,
        "Business Info": business_info,
        "Tax ID": tax_id,
        "E-Invoice Start Date": e_invoice_start_date.strftime("%Y-%m-%d") if e_invoice_start_date else "",
        "Plug In Module": ", ".join(selected_plugins),
        "VPN Info": vpn_info,
        "Module & User License": module_license,
        "Report Design Template": ", ".join(selected_reports),
        "Migration Master Data": migration_master,
        "Migration Outstanding Balance": migration_outstanding,
        "Status": status
    }

    # Create record in database
    df = create_record(form_data)
    st.success(f"✅ Record for {company_name} created successfully!")
    st.session_state.form_submitted = False
    return df

def render_create_form():
    st.session_state.edit_mode = False
    st.session_state.selected_record = None
    
    st.title("Job Order Form")
    
    # Create two columns for the form layout
    left_col, right_col = st.columns(2)
    
    with left_col:
        # User Type Selection
        st.subheader("1. User Type")
        new_user = st.checkbox("New User")
        existing_user = st.checkbox("Existing User")

        if st.session_state.form_submitted and not (new_user or existing_user):
            st.error("Please select a user type")

        # Company Information
        st.subheader("2. Company Information")
        company_name = st.text_input("Company Name*", value="", key="company_name")
        email = st.text_input("Email*", value="", key="email")
        address = st.text_area("Address", value="", key="address")
        business_info = st.text_input("Business Info", value="", key="business_info")
        tax_id = st.text_input("Tax ID", value="", key="tax_id")
        e_invoice_start_date = st.date_input("E-Invoice Start Date", value=None, key="e_invoice_start_date")

    with right_col:
        # Module Information
        st.subheader("3. Module Information")
        st.write("Plug-in Modules:")
        selected_plugins = []
        for plugin in PLUGIN_OPTIONS:
            if st.checkbox(plugin, key=f"plugin_{plugin}"):
                selected_plugins.append(plugin)

        st.write("")
        vpn_info = st.text_input("VPN Information", value="", key="vpn_info")
        module_license = st.text_input("Module & User License", value="", key="module_license")

        # Report Selection
        st.subheader("4. Report Templates")
        selected_reports = []
        for report in REPORT_OPTIONS:
            if st.checkbox(report, key=f"report_{report}"):
                selected_reports.append(report)

    # Migration Information (Full Width)
    st.subheader("5. Migration Details")
    migration_cols = st.columns(2)
    with migration_cols[0]:
        migration_master = st.text_input("Migration Master Data", value="", key="migration_master")
    with migration_cols[1]:
        migration_outstanding = st.text_input("Outstanding Balance", value="", key="migration_outstanding")

    # Status (Full Width)
    st.subheader("6. Status")
    status = st.selectbox("Current Status", [""] + STATUS_OPTIONS, key="status")

    # Save Button
    if st.button("Save Record", use_container_width=True):
        return handle_form_submit(
            new_user, existing_user, company_name, email, address,
            business_info, tax_id, e_invoice_start_date, selected_plugins,
            vpn_info, module_license, selected_reports, migration_master,
            migration_outstanding, status
        )
    return None