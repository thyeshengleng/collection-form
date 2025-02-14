import streamlit as st
from datetime import datetime
from app.utils.database import update_record
from app.config.settings import PLUGIN_OPTIONS, REPORT_OPTIONS, STATUS_OPTIONS
import time

def render_edit_form(record, index):
    st.subheader(f"Edit Record: {record['Company Name']}")
    
    # User Type
    user_type = st.radio(
        "User Type *",
        ["New User", "Existing User"],
        index=0 if record["User Type"] == "New User" else 1
    )
    
    # Company Information
    st.subheader("Company Information")
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
    
    # Plugin Selection
    st.subheader("PLUG IN MODULE *")
    existing_plugins = record["Plug In Module"].split(", ") if record["Plug In Module"] else []
    selected_plugins = []
    for plugin in PLUGIN_OPTIONS:
        if st.checkbox(plugin, key=f"edit_plugin_{plugin}", value=plugin in existing_plugins):
            selected_plugins.append(plugin)
    
    # Additional Information
    st.subheader("Additional Information")
    vpn_info = st.text_input("VPN INFO *", value=record["VPN Info"])
    module_license = st.text_input("MODULE & USER LICENSE *", value=record["Module & User License"])
    
    # Report Selection
    st.markdown("### REPORT DESIGN TEMPLATE *")
    existing_reports = record["Report Design Template"].split(", ") if record["Report Design Template"] else []
    selected_reports = []
    report_cols = st.columns(2)
    for idx, report in enumerate(REPORT_OPTIONS):
        with report_cols[idx % 2]:
            if st.checkbox(report, key=f"edit_report_{report}", value=report in existing_reports):
                selected_reports.append(report)
    
    # Migration Information
    migration_master = st.text_input("MIGRATION MASTER DATA *", value=record["Migration Master Data"])
    migration_outstanding = st.text_input("MIGRATION (OUTSTANDING BALANCE) *", value=record["Migration Outstanding Balance"])
    
    # Status
    status = st.selectbox(
        "Status *",
        STATUS_OPTIONS,
        index=STATUS_OPTIONS.index(record["Status"]) if record["Status"] in STATUS_OPTIONS else 0
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
            df = update_record(index, updated_data)
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