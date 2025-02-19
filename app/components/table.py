import streamlit as st
from app.utils.database import load_records, delete_record
from app.config.settings import STATUS_OPTIONS
import time

def render_view_form(record):
    st.subheader(f"View Record: {record['Company Name']}")
    
    # Display all record details in read-only format
    st.markdown("### Company Information")
    st.text(f"User Type: {record['User Type']}")
    st.text(f"Company Name: {record['Company Name']}")
    st.text(f"Email: {record['Email']}")
    st.text(f"Address: {record['Address']}")
    st.text(f"Business Info: {record['Business Info']}")
    st.text(f"Tax ID: {record['Tax ID']}")
    st.text(f"E-Invoice Start Date: {record['E-Invoice Start Date']}")
    
    st.markdown("### Plug In Module")
    st.text(record['Plug In Module'])
    
    st.markdown("### Additional Information")
    st.text(f"VPN Info: {record['VPN Info']}")
    st.text(f"Module & User License: {record['Module & User License']}")
    
    st.markdown("### Report Design Template")
    st.text(record['Report Design Template'])
    
    st.markdown("### Migration Information")
    st.text(f"Master Data: {record['Migration Master Data']}")
    st.text(f"Outstanding Balance: {record['Migration Outstanding Balance']}")
    
    st.markdown("### Status")
    st.text(record['Status'])
    
    if st.button("Close", use_container_width=True):
        st.session_state.view_mode = False
        st.rerun()

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
                    options=STATUS_OPTIONS
                ),
            },
            disabled=["Company Name", "User Type", "Email", "Status"],
            key="data_editor"
        )
        
        # Handle selected rows
        selected_rows = edited_df[edited_df["Select"] == True]
        if not selected_rows.empty:
            idx = selected_rows.index[0]
            record = df.iloc[idx]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("👁️ View", use_container_width=True):
                    st.session_state.view_mode = True
                    st.session_state.selected_record = idx
                    st.rerun()
            
            with col2:
                if st.button("✏️ Edit", use_container_width=True):
                    st.session_state.edit_mode = True
                    st.session_state.selected_record = idx
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", use_container_width=True):
                    if st.button("⚠️ Confirm Delete"):
                        df = delete_record(idx)
                        st.success(f"Deleted record for {record['Company Name']}")
                        time.sleep(1)
                        st.rerun()
        
        # Show view form if in view mode
        if getattr(st.session_state, 'view_mode', False) and st.session_state.selected_record is not None:
            record = df.iloc[st.session_state.selected_record]
            render_view_form(record)
        
        return df, edited_df
    return None, None 