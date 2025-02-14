import streamlit as st
from datetime import datetime
from config.settings import PLUGIN_OPTIONS, REPORT_OPTIONS, STATUS_OPTIONS
from utils.database import create_record

def render_create_form():
    st.session_state.edit_mode = False
    st.session_state.selected_record = None
    
    # User Type Selection
    st.subheader("User Type")
    new_user = st.checkbox("New User")
    existing_user = st.checkbox("Existing User")

    if st.session_state.form_submitted and not (new_user or existing_user):
        st.error("Please select a user type")

    # Company Information
    st.subheader("Company Information")
    company_name = st.text_input("COMPANY NAME", value="")
    email = st.text_input("EMAIL", value="")
    address = st.text_area("ADDRESS", value="")
    business_info = st.text_input("BUSINESS INFO", value="")
    tax_id = st.text_input("TAX ID", value="")
    e_invoice_start_date = st.date_input("E-INVOICE START DATE", value=None)

    # Plugin Selection
    st.subheader("PLUG IN MODULE")
    selected_plugins = []
    for plugin in PLUGIN_OPTIONS:
        if st.checkbox(plugin):
            selected_plugins.append(plugin)

    # Additional Information
    st.subheader("Additional Information")
    vpn_info = st.text_input("VPN INFO", value="")
    module_license = st.text_input("MODULE & USER LICENSE", value="")

    # Report Selection
    st.markdown("### REPORT DESIGN TEMPLATE *")
    selected_reports = []
    report_cols = st.columns(2)
    for idx, report in enumerate(REPORT_OPTIONS):
        with report_cols[idx % 2]:
            if st.checkbox(report, key=f"report_{report}"):
                selected_reports.append(report)

    # Migration Information
    migration_master = st.text_input("MIGRATION MASTER DATA", value="")
    migration_outstanding = st.text_input("MIGRATION (OUTSTANDING BALANCE)", value="")

    # Status
    status = st.selectbox("Status", [""] + STATUS_OPTIONS)

    # Save Button
    if st.button("Save Record", use_container_width=True):
        return handle_form_submit(
            new_user, existing_user, company_name, email, address,
            business_info, tax_id, e_invoice_start_date, selected_plugins,
            vpn_info, module_license, selected_reports, migration_master,
            migration_outstanding, status
        )
    return None 