import streamlit as st
from app.utils.database import load_records
from app.config.settings import STATUS_OPTIONS
import time

def render_view_form(record):
    # Create a popup overlay and container
    st.markdown(
        """
        <style>
        .popup-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1001;
            backdrop-filter: blur(2px);
        }
        .popup-container {
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
            max-height: 90vh;
            overflow-y: auto;
            z-index: 1002;
        }
        .popup-header {
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
        }
        .popup-close {
            cursor: pointer;
            font-size: 1.5rem;
            color: #666;
        }
        .popup-content {
            margin: 1rem 0;
        }
        .popup-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        .popup-section h4 {
            margin-bottom: 0.5rem;
            color: #333;
        }
        .stButton button {
            width: 100%;
        }
        </style>
        <div class="popup-overlay">
            <div class="popup-container">
                <div class="popup-header">
                    <h3>View Record: {}</h3>
                    <span class="popup-close" onclick="javascript:document.querySelector('.popup-overlay').remove()">×</span>
                </div>
                <div class="popup-content">
        """.format(record['Company Name']),
        unsafe_allow_html=True
    )

    # Form sections with correct field names
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

    # Close button
    if st.button("Close", key="popup_close"):
        st.session_state.view_mode = False
        st.rerun()

    # Close popup container
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_records_table():
    df = load_records()
    
    if not df.empty:
        # Search functionality
        st.subheader("Search Records")
        search_term = st.text_input("Search by Company Name or Email", "")
        
        if search_term:
            df = df[
                df["Company Name"].str.contains(search_term, case=False, na=False) |
                df["Email"].str.contains(search_term, case=False, na=False)
            ]
        
        st.subheader("Existing Records")
        
        # Create interactive table
        view_df = df.copy()
        view_df.insert(0, "Select", False)
        
        edited_df = st.data_editor(
            view_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select to view record details",
                    default=False,
                    width="small"
                ),
                "Company Name": st.column_config.TextColumn("Company Name", width="medium"),
                "User Type": st.column_config.TextColumn("User Type", width="small"),
                "Email": st.column_config.TextColumn("Email", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            },
            disabled=["Company Name", "User Type", "Email", "Status"],
            key="data_editor"
        )
        
        # Handle selected rows
        selected_rows = edited_df[edited_df["Select"] == True]
        if not selected_rows.empty:
            idx = selected_rows.index[0]
            record = df.iloc[idx]
            
            # Single view button
            if st.button("👁️ View Details", use_container_width=True):
                st.session_state.view_mode = True
                st.session_state.selected_record = idx
                st.rerun()
        
        # Show view form if in view mode
        if getattr(st.session_state, 'view_mode', False) and st.session_state.selected_record is not None:
            record = df.iloc[st.session_state.selected_record]
            render_view_form(record)
        
        return df, edited_df
    return None, None 