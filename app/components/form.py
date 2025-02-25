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
    
    # Add PDF Export button at the top
    if st.button("📄 Preview as PDF", use_container_width=True):
        try:
            from app.utils.pdf_generator import generate_pdf
            import tempfile
            import os
            
            # Create form data dictionary for preview
            preview_data = {
                "User Type": "New User" if st.session_state.get('new_user', False) else "Existing User",
                "Company Name": st.session_state.get('company_name', ''),
                "Email": st.session_state.get('email', ''),
                "Address": st.session_state.get('address', ''),
                "Business Info": st.session_state.get('business_info', ''),
                "Tax ID": st.session_state.get('tax_id', ''),
                "E-Invoice Start Date": st.session_state.get('e_invoice_start_date', ''),
                "Plug In Module": ", ".join(st.session_state.get('selected_plugins', [])),
                "VPN Info": st.session_state.get('vpn_info', ''),
                "Module & User License": st.session_state.get('module_license', ''),
                "Report Design Template": ", ".join(st.session_state.get('selected_reports', [])),
                "Migration Master Data": st.session_state.get('migration_master', ''),
                "Migration Outstanding Balance": st.session_state.get('migration_outstanding', ''),
                "Status": st.session_state.get('status', '')
            }
            
            # Create a temporary file for the PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                generate_pdf(preview_data, tmp_file.name)
                
                # Read the generated PDF
                with open(tmp_file.name, 'rb') as pdf_file:
                    pdf_bytes = pdf_file.read()
                
                # Create download button
                company_name = preview_data['Company Name'] or 'new_record'
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=f"{company_name}_job_order.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # Clean up the temporary file
                os.unlink(tmp_file.name)
                
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
    
    # User Type Selection
    st.subheader("User Type")
    new_user = st.checkbox("New User")
    existing_user = st.checkbox("Existing User")

    if st.session_state.form_submitted and not (new_user or existing_user):
        st.error("Please select a user type")

    # Company Information
    st.subheader("Company Information")
    company_name = st.text_input("COMPANY NAME", value="", key="company_name")
    email = st.text_input("EMAIL", value="", key="email")
    address = st.text_area("ADDRESS", value="", key="address")
    business_info = st.text_input("BUSINESS INFO", value="", key="business_info")
    tax_id = st.text_input("TAX ID", value="", key="tax_id")
    e_invoice_start_date = st.date_input("E-INVOICE START DATE", value=None, key="e_invoice_start_date")

    # Plugin Selection
    st.subheader("PLUG IN MODULE")
    selected_plugins = []
    for plugin in PLUGIN_OPTIONS:
        if st.checkbox(plugin):
            selected_plugins.append(plugin)

    # Additional Information
    st.subheader("Additional Information")
    vpn_info = st.text_input("VPN INFO", value="", key="vpn_info")
    module_license = st.text_input("MODULE & USER LICENSE", value="", key="module_license")

    # Report Selection
    st.markdown("### REPORT DESIGN TEMPLATE *")
    selected_reports = []
    report_cols = st.columns(2)
    for idx, report in enumerate(REPORT_OPTIONS):
        with report_cols[idx % 2]:
            if st.checkbox(report, key=f"report_{report}"):
                selected_reports.append(report)

    # Migration Information
    migration_master = st.text_input("MIGRATION MASTER DATA", value="", key="migration_master")
    migration_outstanding = st.text_input("MIGRATION (OUTSTANDING BALANCE)", value="", key="migration_outstanding")

    # Status
    status = st.selectbox("Status", [""] + STATUS_OPTIONS, key="status")

    # Save Button
    if st.button("Save Record", use_container_width=True):
        return handle_form_submit(
            new_user, existing_user, company_name, email, address,
            business_info, tax_id, e_invoice_start_date, selected_plugins,
            vpn_info, module_license, selected_reports, migration_master,
            migration_outstanding, status
        )
    return None