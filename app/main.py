import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
import pyodbc
from sqlalchemy import create_engine
from app.utils.database import load_records, save_records, create_record, update_record, delete_record
from app.components.form import render_create_form
from app.components.table import render_records_table
from app.components.edit_form import render_edit_form

def render_db_form():
    st.subheader("Database Connection")
    
    # View Data button
    if st.button("👁️ View Database Data", use_container_width=True):
        try:
            # Create SQLAlchemy connection string
            params = urllib.parse.quote_plus(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-RMNV9QV\\A2006;'
                'DATABASE=AED_AssignmentOne;'
                'UID=sa;'
                'PWD=oCt2005-ShenZhou6_A2006;'
                'Trusted_Connection=no;'
            )
            
            # Create SQLAlchemy engine
            engine = create_engine(
                f"mssql+pyodbc:///?odbc_connect={params}",
                pool_pre_ping=True,  # Check connection before using
                pool_recycle=3600    # Recycle connections after 1 hour
            )
            
            # Try to connect and fetch data
            with st.spinner("Connecting to database..."):
                st.info("Attempting to connect to SQL Server...")
                
                # Test connection first
                with engine.connect() as conn:
                    st.info("Connected! Fetching data...")
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
                
                # Display data
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
            Please check:
            1. SQL Server instance name is correct (A2006)
            2. SQL Server service is running
            3. SQL Server Browser service is running
            4. Windows Authentication is enabled
            5. TCP/IP protocol is enabled
            """)

def render_popup_view(record):
    # Create a popup overlay and container
    popup_html = f"""
        <style>
        .popup-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1001;
            backdrop-filter: blur(2px);
        }}
        .popup-container {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 800px;
            max-height: 85vh;
            overflow-y: auto;
            z-index: 1002;
        }}
        .popup-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #eee;
            position: sticky;
            top: 0;
            background: white;
            z-index: 1003;
        }}
        .popup-close {{
            cursor: pointer;
            font-size: 1.5rem;
            color: #666;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background 0.3s;
        }}
        .popup-close:hover {{
            background: #f0f0f0;
        }}
        .popup-content {{
            margin: 1rem 0;
        }}
        .popup-section {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
        }}
        .popup-section h4 {{
            margin-bottom: 0.5rem;
            color: #333;
        }}
        </style>
        <div class="popup-overlay" onclick="closePopup()">
            <div class="popup-container" onclick="event.stopPropagation()">
                <div class="popup-header">
                    <h3>View Record: {record.get('Company Name', '')}</h3>
                    <span class="popup-close" onclick="closePopup()">×</span>
                </div>
                <div class="popup-content">
        """
    
    # Add JavaScript for closing popup
    popup_html += """
        <script>
        function closePopup() {
            document.querySelector('.popup-overlay').remove();
            // Tell Streamlit to update
            setTimeout(function() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
            }, 100);
        }
        </script>
    """
    
    st.markdown(popup_html, unsafe_allow_html=True)

    # Form sections
    sections = [
        ("User Type", ["User Type"]),
        ("Company Information", [
            "Company Name", "Email", "Address", 
            "Business Info", "Tax ID", "E-Invoice Start Date"
        ]),
        ("Plug In Module", ["Plug In Module"]),
        ("Additional Information", ["VPN Info", "Module & User License"]),
        ("Report Design Template", ["Report Design Template"]),
        ("Migration Information", ["Migration Master Data", "Migration Outstanding Balance"]),
        ("Status", ["Status"])
    ]

    # Display sections
    for section_title, fields in sections:
        st.markdown(f'<div class="popup-section">', unsafe_allow_html=True)
        st.markdown(f"#### {section_title}")
        for field in fields:
            if field in ["Address", "Plug In Module", "Report Design Template"]:
                st.text_area(field, value=record.get(field, ''), disabled=True)
            else:
                st.text_input(field, value=record.get(field, ''), disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Close button at bottom
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Close", use_container_width=True, key="popup_close"):
            st.session_state.view_mode = False
            st.rerun()

    # Close popup container
    st.markdown("</div></div>", unsafe_allow_html=True)

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
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = False
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
            # Handle selected rows
            selected_rows = edited_df[edited_df["Select"] == True]
            if not selected_rows.empty:
                idx = selected_rows.index[0]
                record = df.iloc[idx]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👁️ View Details", use_container_width=True):
                        st.session_state.view_mode = True
                        st.session_state.selected_record = idx
                        st.rerun()
                
                with col2:
                    if st.button("✏️ Edit Selected", use_container_width=True):
                        st.session_state.edit_mode = True
                        st.session_state.selected_record = idx
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete Selected", use_container_width=True):
                        if st.button("⚠️ Confirm Delete"):
                            df = delete_record(idx)
                            st.success(f"Deleted record for {record['Company Name']}")
                            time.sleep(1)
                            st.rerun()

            # Show view form if in view mode
            if st.session_state.view_mode and st.session_state.selected_record is not None:
                record = df.iloc[st.session_state.selected_record]
                render_popup_view(record)

            # Show edit form if in edit mode
            if st.session_state.edit_mode and st.session_state.selected_record is not None:
                record = df.iloc[st.session_state.selected_record]
                render_edit_form(record, st.session_state.selected_record)

if __name__ == "__main__":
    main() 