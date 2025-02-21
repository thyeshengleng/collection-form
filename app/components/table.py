import streamlit as st
from app.utils.database import load_records
from app.config.settings import STATUS_OPTIONS
import time

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
        view_df.insert(1, "Actions", "View Details")
        
        edited_df = st.data_editor(
            view_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select to view, edit or delete",
                    default=False,
                    width="small"
                ),
                "Actions": st.column_config.ButtonColumn(
                    "Actions",
                    help="Click to view details",
                    width="small"
                ),
                "Company Name": st.column_config.TextColumn("Company Name", width="medium"),
                "User Type": st.column_config.TextColumn("User Type", width="small"),
                "Email": st.column_config.TextColumn("Email", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            },
            disabled=["Company Name", "User Type", "Email", "Status", "Actions"],
            key="data_editor"
        )
        
        # Handle view details button click
        clicked_rows = edited_df[edited_df["Actions"].eq("View Details")]
        if not clicked_rows.empty:
            with st.expander("Record Details", expanded=True):
                selected_record = df.loc[clicked_rows.index[0]]
                for column, value in selected_record.items():
                    st.write(f"**{column}:** {value}")
        
        return df, edited_df
    return None, None