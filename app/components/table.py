import streamlit as st
from app.utils.database import load_records
from app.config.settings import STATUS_OPTIONS
import time

def render_view_form(record):
    # Create a dialog-like container
    st.markdown(
        """
        <style>
        .dialog-container {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1000;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            width: 80%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
        }
        .dialog-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 999;
        }
        .dialog-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .dialog-content {
            padding: 20px 0;
        }
        .close-button {
            position: absolute;
            top: 20px;
            right: 20px;
            cursor: pointer;
        }
        </style>
        <div class="dialog-overlay"></div>
        <div class="dialog-container">
            <div class="dialog-content">
        """,
        unsafe_allow_html=True
    )
    
    # Close button in the top-right corner
    col1, col2 = st.columns([6,1])
    with col1:
        st.subheader(f"View Record: {record['Company Name']}")
    with col2:
        if st.button("✖️", key="close_top"):
            st.session_state.view_mode = False
            st.rerun()
    
    # Form content
    with st.container():
        # User Type
        st.markdown("### User Type")
        st.text_input("User Type", value=record['User Type'], disabled=True)
        
        # Company Information
        st.markdown("### Company Information")
        st.text_input("Company Name", value=record['Company Name'], disabled=True)
        st.text_input("Email", value=record['Email'], disabled=True)
        st.text_area("Address", value=record['Address'], disabled=True)
        st.text_input("Business Info", value=record['Business Info'], disabled=True)
        st.text_input("Tax ID", value=record['Tax ID'], disabled=True)
        st.text_input("E-Invoice Start Date", value=record['E-Invoice Start Date'], disabled=True)
        
        # Plugin Information
        st.markdown("### Plug In Module")
        st.text_area("Selected Plugins", value=record['Plug In Module'], disabled=True)
        
        # Additional Information
        st.markdown("### Additional Information")
        st.text_input("VPN Info", value=record['VPN Info'], disabled=True)
        st.text_input("Module & User License", value=record['Module & User License'], disabled=True)
        
        # Report Information
        st.markdown("### Report Design Template")
        st.text_area("Selected Reports", value=record['Report Design Template'], disabled=True)
        
        # Migration Information
        st.markdown("### Migration Information")
        st.text_input("Master Data", value=record['Migration Master Data'], disabled=True)
        st.text_input("Outstanding Balance", value=record['Migration Outstanding Balance'], disabled=True)
        
        # Status
        st.markdown("### Status")
        st.text_input("Current Status", value=record['Status'], disabled=True)
    
    # Close button at bottom
    if st.button("Close", use_container_width=True, key="close_bottom"):
        st.session_state.view_mode = False
        st.rerun()
    
    # Close the dialog container
    st.markdown("</div></div>", unsafe_allow_html=True)

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