import streamlit as st
from datetime import datetime
from app.config.settings import PLUGIN_OPTIONS, REPORT_OPTIONS, STATUS_OPTIONS#IMPLEMENTATION_OPTIONS, MASTER_DATA_OPTIONS, MIGRATION_OPTIONS
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
    st.write("Please specify the required modules:")
    
    # Convert checkboxes to text inputs for more flexibility
    st.text_area("Plug-in Modules Required:", help="Enter each module on a new line", key="plugins_text")
    selected_plugins = [plugin.strip() for plugin in st.session_state.get("plugins_text", "").split("\n") if plugin.strip()]
    
    vpn_info = st.text_input("VPN Information", value="", key="vpn_info")
    module_license = st.text_input("Module & User License", value="", key="module_license")
    
    # Report Templates
    st.markdown("---")
    st.subheader("Report Templates")
    st.write("Please specify the required report templates:")
    st.text_area("Report Templates Required:", help="Enter each template on a new line", key="reports_text")
    selected_reports = [report.strip() for report in st.session_state.get("reports_text", "").split("\n") if report.strip()]
    
    # Implementation Section
    st.markdown("---")
    st.subheader("B. IMPLEMENTATION")
    st.write("(Optional - You can provide your existing or desired A4/A5 Letter Format later)")
    
    # Document Numbering Format Fields
    st.text_input("1. SALES ORDER DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_sales_order")
    st.text_input("2. DELIVERY ORDER DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_delivery_order")
    st.text_input("3. SALES INVOICE DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_sales_invoice")
    st.text_input("4. PICKING LIST DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_picking_list")
    st.text_input("5. PURCHASE ORDER DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_purchase_order")
    st.text_input("6. CASH SALES DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_cash_sales")
    st.text_input("7. QUOTATION DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_quotation")
    st.text_input("8. OFFICIAL RECEIPT DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_official_receipt")
    st.text_input("9. PAYMENT VOUCHER DOCUMENT NUMBERING FORMAT: (Optional)", key="impl_payment_voucher")
    
    # Master Data Section
    st.markdown("---")
    st.subheader("C. MASTER DATA")
    st.write("(Kindly provide us below data in excel format!)")
    
    migration_master = st.selectbox("1. CHART OF ACCOUNT: (Your COA # only/Autoccount COA standard template)", [" ", "Not yet", "Done"], key="master_coa")
    st.selectbox("2. DEBTOR: (Your List of Customer)", [" ", "Not yet", "Done"], key="master_debtor")
    st.selectbox("3. CREDITOR: (Your List of Supplier)", [" ", "Not yet", "Done"], key="master_creditor")
    st.selectbox("4. STOCK ITEM: (Your List of Items/Products)", [" ", "Not yet", "Done"], key="master_stock")
   
    # Migration Section
    st.markdown("---")
    st.subheader("D. MIGRATION")
    st.write("(Kindly provide us outstanding data in excel format!)")
    
    migration_outstanding = st.text_area("1. DEBTOR AGING: (Outstanding Debtor Invoice, OR, CN, DN)")
    st.text_area("2. CREDITOR AGING: (Outstanding Creditor Invoice, PV, CN, DN)")
    st.text_area("3. TRIAL BALANCE REPORT: (For Account Opening Purpose)")
    st.text_area("4. BALANCE SHEET REPORT: (For Account Opening Purpose)")
    st.text_area("5. STOCK BALANCE: (For Item Opening Balance Purpose)")
    st.text_area("6. SO/PO OUTSTANDING: (Outstanding SO/PO by Item, and amount)")
    
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