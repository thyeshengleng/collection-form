import streamlit as st
from datetime import datetime
from app.config.settings import PLUGIN_OPTIONS, REPORT_OPTIONS, STATUS_OPTIONS, IMPLEMENTATION_OPTIONS, MASTER_DATA_OPTIONS
from app.utils.database import create_record

def handle_form_submit(new_user, existing_user, company_name, company_email, company_address,
                      company_phone, tin_number, msic_code, nature_of_business,
                      roc_number, pic_name, pic_phone, financial_year,
                      e_invoice_start_date, existing_software, selected_plugins,
                      vpn_info, module_license, selected_reports, migration_master,
                      migration_outstanding, status):
    # Validate required fields
    if not (new_user or existing_user):
        st.error("Please select a user type")
        return None
    
    if not company_name or not company_email:
        st.error("Company Name and Email are required")
        return None

    # Create form data dictionary
    form_data = {
        "User Type": "New User" if new_user else "Existing User",
        "Company Name": company_name,
        "Company Email": company_email,
        "Company Address": company_address,
        "Company Phone": company_phone,
        "TIN Number": tin_number,
        "MSIC Code": msic_code,
        "Nature of Business": nature_of_business,
        "ROC Reg. Number": roc_number,
        "PIC Name": pic_name,
        "PIC Phone": pic_phone,
        "Financial Year": financial_year,
        "E-Invoice Start Date": e_invoice_start_date.strftime("%Y-%m-%d") if e_invoice_start_date else "",
        "Existing Software": existing_software,
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
    st.markdown("---")
    
    # User Type Selection
    st.subheader("User Type")
    col1, col2 = st.columns(2)
    with col1:
        new_user = st.checkbox("New User")
    with col2:
        existing_user = st.checkbox("Existing User")

    if st.session_state.form_submitted and not (new_user or existing_user):
        st.error("Please select a user type")
    
    # Company Information
    st.markdown("---")
    st.subheader("A. COMPANY INFORMATION")
    
    # Company Information Fields
    company_name = st.text_input("1. COMPANY NAME:", value="", key="company_name")
    company_email = st.text_input("2. COMPANY EMAIL:", value="", key="company_email")
    date_collect = st.date_input("3. DATE COLLECT:", value=None, key="date_collect")
    company_address = st.text_area("4. COMPANY ADDRESS:", value="", key="company_address")
    company_phone = st.text_input("5. COMPANY PHONE:", value="", key="company_phone")
    tin_number = st.text_input("6. TIN NUMBER:", value="", key="tin_number")
    msic_code = st.text_input("7. MSIC CODE:", value="", key="msic_code")
    nature_of_business = st.text_input("8. NATURE OF BUSINESS:", value="", key="nature_of_business")
    roc_number = st.text_input("9. ROC REG. NUMBER:", value="", key="roc_number")
    pic_name = st.text_input("10. PIC NAME:", value="", key="pic_name")
    pic_phone = st.text_input("11. PIC PHONE:", value="", key="pic_phone")
    financial_year = st.text_input("12. FINANCIAL YEAR:", value="", key="financial_year")
    e_invoice_start_date = st.date_input("13. E-INVOICE START DATE:", value=None, key="e_invoice_start_date")
    existing_software = st.text_input("14. EXISTING OLD SOFTWARE (SQL,MILLION,UBS):", value="", key="existing_software")
    
    # Removed redundant fields that were duplicating information
    
    # Module Information
    st.markdown("---")
    st.subheader("Module Information")
    st.write("Plug-in Modules:")
    selected_plugins = []
    cols = st.columns(3)
    for i, plugin in enumerate(PLUGIN_OPTIONS):
        with cols[i % 3]:
            if st.checkbox(plugin, key=f"plugin_{plugin}"):
                selected_plugins.append(plugin)
    
    vpn_info = st.text_input("VPN Information", value="", key="vpn_info")
    module_license = st.text_input("Module & User License", value="", key="module_license")
    
    # Report Selection
    st.markdown("---")
    st.subheader("Report Templates")
    selected_reports = []
    report_cols = st.columns(2)
    for i, report in enumerate(REPORT_OPTIONS):
        with report_cols[i % 2]:
            if st.checkbox(report, key=f"report_{report}"):
                selected_reports.append(report)
    
    # Implementation Section
    st.markdown("---")
    st.subheader("B. IMPLEMENTATION")
    st.write("(Kindly provide us your existing or desired A4/A5 Letter Format)")
    
    implementation_data = {}
    for option in IMPLEMENTATION_OPTIONS:
        implementation_data[option] = st.text_input(f"{option} Document Numbering Format:", key=f"impl_{option}")
    
    # Master Data Section
    st.markdown("---")
    st.subheader("C. MASTER DATA")
    st.write("(Kindly provide us below data in excel format!)")
    
    master_data = {}
    descriptions = {
        "CHART OF ACCOUNT": "(Your COA # only/Autoccount COA standard template)",
        "DEBTOR": "(Your List of Customer)",
        "CREDITOR": "(Your List of Supplier)",
        "STOCK ITEM": "(Your List of Items/Products)"
    }
    
    for option in MASTER_DATA_OPTIONS:
        st.write(f"{option} {descriptions[option]}")
        master_data[f"{option}_data"] = st.text_input(f"{option} Data", key=f"master_data_{option}")
        st.markdown("<hr style='margin: 10px 0px'>", unsafe_allow_html=True)
    
    # Migration Section
    st.markdown("---")
    st.subheader("D. MIGRATION")
    st.write("(Kindly provide us outstanding data in excel format!)")
    
    migration_data = {}
    descriptions = {
        "DEBTOR AGING": "Outstanding Debtor Invoice ,OR, CN, DN",
        "CREDITOR AGING": "Outstanding Creditor Invoice ,PV, CN, DN",
        "TRIAL BALANCE REPORT": "For Account Opening Purpose",
        "BALANCE SHEET REPORT": "For Account Opening Purpose",
        "STOCK BALANCE": "For Item Opening Balance Purpose",
        "SO/PO OUTSTANDING": "Outstanding SO/PO by Item, and amount"
    }
    
    for option in MIGRATION_OPTIONS:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{option}: {descriptions[option]}")
        with col2:
            migration_data[option] = st.checkbox("", key=f"migration_{option}")
    
    # Status
    st.markdown("---")
    st.subheader("Status")
    status = st.selectbox("Current Status", [""] + STATUS_OPTIONS, key="status")
    
    st.markdown("---")

    # Save Button
    if st.button("Save Record", use_container_width=True):
        return handle_form_submit(
            new_user, existing_user, company_name, company_email, company_address,
            company_phone, tin_number, msic_code, nature_of_business,
            roc_number, pic_name, pic_phone, financial_year,
            e_invoice_start_date, existing_software, selected_plugins,
            vpn_info, module_license, selected_reports, migration_master,
            migration_outstanding, status
        )
    return None