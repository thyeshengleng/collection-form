import streamlit as st
import pandas as pd
from datetime import datetime
import time
from app.utils.database import load_records, save_records, create_record, update_record, delete_record

def collect_implementation_form_data():
    # Collect all form data into a dictionary
    form_data = {}
    
    # Company Information
    form_data["Company Name"] = st.session_state.get("company_name", "")
    form_data["Autocount Module"] = st.session_state.get("module", "")
    form_data["Start Date"] = st.session_state.get("start_date", datetime.now().date()).strftime("%Y-%m-%d")
    form_data["Training Date"] = st.session_state.get("training_date", datetime.now().date()).strftime("%Y-%m-%d")
    form_data["Complete Date"] = st.session_state.get("complete_date", datetime.now().date()).strftime("%Y-%m-%d")
    form_data["Job Assigned"] = st.session_state.get("job_assigned", "")
    
    # Collect all step data
    for step in range(1, 35):  # All steps from 1-34
        # Status
        status_key = f"status_{step}"
        if status_key in st.session_state:
            form_data[f"Step {step} Status"] = st.session_state[status_key]
        
        # Date
        date_key = f"date_{step}"
        if date_key in st.session_state:
            form_data[f"Step {step} Date"] = st.session_state[date_key].strftime("%Y-%m-%d")
        
        # Version/Name (only for steps 1-4)
        if step < 5:
            version_key = f"version_{step}"
            if version_key in st.session_state:
                form_data[f"Step {step} Version"] = st.session_state[version_key]
    
    # Server info
    server_keys = ["server_name", "database_name", "product_id", "access_key", "radmin_vpn"]
    for key in server_keys:
        if key in st.session_state:
            form_data[key.replace("_", " ").title()] = st.session_state[key]
            date_key = f"{key}_date"
            if date_key in st.session_state:
                form_data[f"{key.replace('_', ' ').title()} Date"] = st.session_state[date_key].strftime("%Y-%m-%d")
    
    # Additional tasks
    if 'additional_tasks' in st.session_state:
        for i, task in enumerate(st.session_state.additional_tasks):
            if task.strip():
                form_data[f"Additional Task {i+1}"] = task
                if 'additional_task_dates' in st.session_state and i < len(st.session_state.additional_task_dates):
                    if st.session_state.additional_task_dates[i]:
                        form_data[f"Additional Task {i+1} Date"] = st.session_state.additional_task_dates[i].strftime("%Y-%m-%d")
    
    return form_data

def render_implementation_table():
    df = load_records()
    
    if not df.empty:
        # Filter for implementation records (simple heuristic - has 'Step 1 Status' field)
        impl_df = df[df.apply(lambda row: 'Step 1 Status' in row, axis=1)]
        
        if impl_df.empty:
            st.info("No implementation records found.")
            return None, None
        
        # Search functionality
        st.subheader("Search Implementation Records")
        search_term = st.text_input("Search by Company Name", "")
        
        if search_term:
            impl_df = impl_df[
                impl_df["Company Name"].str.contains(search_term, case=False, na=False)
            ]
        
        st.subheader("Existing Implementation Records")
        
        # Create interactive table
        view_df = impl_df.copy()
        view_df.insert(0, "Select", False)
        
        # Select only relevant columns for display
        display_columns = ["Select", "Company Name", "Autocount Module", "Start Date", "Complete Date"]
        display_df = view_df[display_columns] if all(col in view_df.columns for col in display_columns) else view_df
        
        edited_df = st.data_editor(
            display_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select to view, edit or delete",
                    default=False,
                    width="small"
                ),
                "Company Name": st.column_config.TextColumn("Company Name", width="medium"),
                "Autocount Module": st.column_config.TextColumn("Module", width="small"),
                "Start Date": st.column_config.DateColumn("Start Date", width="small"),
                "Complete Date": st.column_config.DateColumn("Complete Date", width="small"),
            },
            disabled=[col for col in display_columns if col != "Select"],
            key="implementation_editor"
        )
        
        return impl_df, edited_df
    return None, None

def render_implementation_form():
    # Company Information
    company_name = st.text_input("COMPANY NAME")
    module = st.text_input("AUTOCOUNT MODULE")
    start_date = st.date_input("ACTUAL START DATE")
    training_date = st.date_input("TRAINING DATE")
    complete_date = st.date_input("ESTIMATED COMPLETE DATE")
    job_assigned = st.text_input("JOB ASSIGNED")
    
    # Create a table-like structure
    st.markdown("### Installation & Implementation Progress")
    
    st.markdown("#### INSTALLATION:")
    
    # Installation steps
    installation_steps = [
        (1, "AUTOCOUNT SYSTEM"),
        (2, "AUTOCOUNT CLIENT PC"),
        (3, "VPN"),
        (4, "SQL SERVER"),
        (5, "LICENSE ACTIVATION")
    ]
    
    for step, desc in installation_steps:
        st.markdown(f"**{step}. {desc}**")
        # Special handling for VPN step
        if step == 3:  # VPN step
            # Replace selectbox with text_input that has suggestions
            vpn_options = ["", "ZEROTIER", "RADMIN"]
            default_vpn = st.session_state.get(f"version_{step}", "")
            
            # Create a container for the custom input solution
            vpn_container = st.container()
            
            # Add a selectbox for predefined options with an "Other" option
            vpn_selection = vpn_container.selectbox(
                "VPN Name",
                vpn_options + ["Other (specify)"],
                index=vpn_options.index(default_vpn) if default_vpn in vpn_options else 0,
                key=f"vpn_selection_{step}"
            )
            
            # Show text input if "Other" is selected
            if vpn_selection == "Other (specify)":
                version = vpn_container.text_input(
                    "Enter custom VPN name",
                    value=st.session_state.get(f"custom_vpn_{step}", ""),
                    key=f"custom_vpn_{step}"
                )
                # Store the custom value in the original key for consistency
                st.session_state[f"version_{step}"] = version
            else:
                # Use the selected predefined option
                version = vpn_selection
                st.session_state[f"version_{step}"] = version
        elif step < 5:  # Only show Version/Name for steps 1-4
            version = st.text_input("Version/Name", key=f"version_{step}")
        # For steps 5 and above, we skip the Version/Name input field as requested
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()

    
    st.markdown("#### IMPLEMENTATION:")
    
    # Implementation steps
    implementation_steps = [
        (6, "DATABASE INSTANT NAME"),
        (7, "SETUP COMPANY PROFILE / LOGO / HEADER"),
        (8, "SETUP CHART OF ACCOUNT")
    ]
    
    for step, desc in implementation_steps:
        st.markdown(f"**{step}. {desc}**")
        # Special handling for VPN step
        if step == 3:  # VPN step
            # Replace selectbox with text_input that has suggestions
            vpn_options = ["", "ZEROTIER", "RADMIN"]
            default_vpn = st.session_state.get(f"version_{step}", "")
            
            # Create a container for the custom input solution
            vpn_container = st.container()
            
            # Add a selectbox for predefined options with an "Other" option
            vpn_selection = vpn_container.selectbox(
                "VPN Name",
                vpn_options + ["Other (specify)"],
                index=vpn_options.index(default_vpn) if default_vpn in vpn_options else 0,
                key=f"vpn_selection_{step}"
            )
            
            # Show text input if "Other" is selected
            if vpn_selection == "Other (specify)":
                version = vpn_container.text_input(
                    "Enter custom VPN name",
                    value=st.session_state.get(f"custom_vpn_{step}", ""),
                    key=f"custom_vpn_{step}"
                )
                # Store the custom value in the original key for consistency
                st.session_state[f"version_{step}"] = version
            else:
                # Use the selected predefined option
                version = vpn_selection
                st.session_state[f"version_{step}"] = version
        elif step < 5:  # Only show Version/Name for steps 1-4
            version = st.text_input("Version/Name", key=f"version_{step}")
        # For steps 5 and above, we skip the Version/Name input field as requested
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()
    
    # MASTER DATA section
    st.markdown("#### MASTER DATA (GL, AR, AP, ITEM):")
    
    # Master Data steps
    master_data_steps = [
        (9, "CHART OF ACCOUNT"),
        (10, "DEBTOR"),
        (11, "CREDITOR"),
        (12, "STOCK ITEM")
    ]
    
    for step, desc in master_data_steps:
        st.markdown(f"**{step}. {desc}**")
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()
    
    # PRINTABLE LETTER DESIGN section
    st.markdown("#### PRINTABLE LETTER DESIGN:")
    
    # Printable Letter Design steps
    letter_design_steps = [
        (13, "SALES ORDER"),
        (14, "DELIVERY ORDER"),
        (15, "SALES INVOICE"),
        (16, "PICKING LIST"),
        (17, "PURCHASE ORDER"),
        (18, "CASH SALES"),
        (19, "QUOTATION"),
        (20, "OFFICIAL RECEIPT"),
        (21, "PAYMENT VOUCHER")
    ]
    
    for step, desc in letter_design_steps:
        st.markdown(f"**{step}. {desc}**")
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()
    
    # MIGRATION section
    st.markdown("#### MIGRATION (OUTSTANDING BALANCE):")
    
    # Migration steps
    migration_steps = [
        (22, "DEBTOR AGING"),
        (23, "CREDITOR AGING"),
        (24, "TRIAL BALANCE REPORT"),
        (25, "BALANCE SHEET REPORT"),
        (26, "STOCK BALANCE REPORT"),
        (27, "SO/PO OUTSTANDING")
    ]
    
    for step, desc in migration_steps:
        st.markdown(f"**{step}. {desc}**")
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()
    
    # CONFIGURATION section
    st.markdown("#### CONFIGURATION:")
    
    # Configuration steps
    configuration_steps = [
        (28, "VPN SETTING"),
        (29, "USER ACCESS RIGHT SETTING"),
        (30, "REPORT/COLUMN CHOOSER LAYOUT SETTING"),
        (31, "E-INVOICE SETUP & CONFIGURATION")
    ]
    
    for step, desc in configuration_steps:
        st.markdown(f"**{step}. {desc}**")
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()
    
    # TRAINING section
    st.markdown("#### TRAINING:")
    
    # Training steps
    training_steps = [
        (32, "ACCOUNT"),
        (33, "STOCK"),
        (34, "PLUG IN")
    ]
    
    for step, desc in training_steps:
        st.markdown(f"**{step}. {desc}**")
        status = st.selectbox(
            "Status",
            ["PENDING", "DONE", "NONE"],
            key=f"status_{step}"
        )
        date = st.date_input("Completion Date", key=f"date_{step}")
        st.divider()
    
    # AUTOCOUNT SERVER / DATABASE INFO section
    st.markdown("#### AUTOCOUNT SERVER / DATABASE INFO:")
    
    # Create a table-like structure for server info
    server_info = [
        (1, "SERVER NAME:", "server_name"),
        (2, "DATABASE NAME:", "database_name"),
        (3, "PRODUCT ID :", "product_id"),
        (4, "ACCESS KEY:", "access_key"),
        (5, "RADMIN VPN :", "radmin_vpn")
    ]
    
    # Display each server info field with date
    for num, label, key in server_info:
        st.markdown(f"**{num}. {label}**")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            value = st.text_input("Value", key=key)
        
        with col2:
            date = st.date_input("Date Complete", key=f"{key}_date")
    
    # ADDITIONAL TASKS section
    st.markdown("#### ADDITIONAL TASKS:")
    
    # Initialize additional tasks in session state if not already present
    if 'additional_tasks' not in st.session_state:
        st.session_state.additional_tasks = [""]
    if 'additional_task_dates' not in st.session_state:
        st.session_state.additional_task_dates = [None]
    
    # Create a table-like structure for additional tasks
    for i in range(len(st.session_state.additional_tasks)):
        task_num = i + 1
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Task description input
            task_desc = st.text_input(
                f"Task {task_num}", 
                value=st.session_state.additional_tasks[i],
                key=f"additional_task_{i}"
            )
            # Update session state
            st.session_state.additional_tasks[i] = task_desc
        
        with col2:
            # Date completion field instead of status
            completion_date = st.date_input(
                "Date Complete",
                value=st.session_state.additional_task_dates[i],
                key=f"additional_task_date_{i}"
            )
            # Update session state
            st.session_state.additional_task_dates[i] = completion_date
        
        # Only show divider if task is not empty
        if task_desc.strip():
            st.divider()
    
    # Add button to add more tasks
    if st.button("+ Add Task"):
        st.session_state.additional_tasks.append("")
        st.session_state.additional_task_dates.append(None)
        st.rerun()
    
    # CRUD Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        # Submit Button
        if st.button("Submit Implementation Form", use_container_width=True):
            # Collect form data
            form_data = collect_implementation_form_data()
            
            # Create record in database
            df = create_record(form_data)
            st.success("✅ Implementation form submitted successfully!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        # View Records Button
        if st.button("View Implementation Records", use_container_width=True):
            st.session_state.view_implementation_records = True
            st.rerun()
    
    # View/Edit/Delete Implementation Records
    if st.session_state.get("view_implementation_records", False):
        st.markdown("---")
        st.subheader("Implementation Records")
        
        impl_df, edited_df = render_implementation_table()
        
        if impl_df is not None and edited_df is not None:
            # Handle selected rows
            selected_rows = edited_df[edited_df["Select"] == True]
            if not selected_rows.empty:
                idx = selected_rows.index[0]
                record = impl_df.iloc[idx]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit Selected", use_container_width=True):
                        st.session_state.edit_implementation_mode = True
                        st.session_state.selected_implementation_record = idx
                        st.rerun()
                
                with col2:
                    if st.button("👁️ View Details", use_container_width=True):
                        st.session_state.view_implementation_mode = True
                        st.session_state.selected_implementation_record = idx
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete Selected", use_container_width=True):
                        delete_confirmation = st.button("⚠️ Confirm Delete")
                        if delete_confirmation:
                            df = delete_record(idx)
                            st.success(f"Deleted implementation record for {record['Company Name']}")
                            time.sleep(1)
                            st.rerun()
            
            # Show detailed view if in view mode
            if st.session_state.get("view_implementation_mode", False) and st.session_state.get("selected_implementation_record") is not None:
                st.markdown("---")
                st.subheader(f"View Implementation Record: {impl_df.iloc[st.session_state.selected_implementation_record]['Company Name']}")
                
                # Display all record details
                record = impl_df.iloc[st.session_state.selected_implementation_record]
                for column, value in record.items():
                    if column != "Select":
                        st.text_input(column, value=value, disabled=True)
                
                if st.button("Close View", use_container_width=True):
                    st.session_state.view_implementation_mode = False
                    st.rerun()
            
            # Show edit form if in edit mode
            if st.session_state.get("edit_implementation_mode", False) and st.session_state.get("selected_implementation_record") is not None:
                st.markdown("---")
                st.subheader(f"Edit Implementation Record: {impl_df.iloc[st.session_state.selected_implementation_record]['Company Name']}")
                
                # Pre-fill form with existing data
                record = impl_df.iloc[st.session_state.selected_implementation_record]
                
                # Set session state values from record
                for key, value in record.items():
                    if key.startswith("Step") and key.endswith("Status"):
                        step_num = int(key.split(" ")[1])
                        st.session_state[f"status_{step_num}"] = value
                    elif key.startswith("Step") and key.endswith("Date"):
                        step_num = int(key.split(" ")[1])
                        try:
                            st.session_state[f"date_{step_num}"] = datetime.strptime(value, "%Y-%m-%d").date()
                        except:
                            st.session_state[f"date_{step_num}"] = datetime.now().date()
                    elif key.startswith("Step") and key.endswith("Version"):
                        step_num = int(key.split(" ")[1])
                        st.session_state[f"version_{step_num}"] = value
                
                # Set company info
                st.session_state["company_name"] = record.get("Company Name", "")
                st.session_state["module"] = record.get("Autocount Module", "")
                try:
                    st.session_state["start_date"] = datetime.strptime(record.get("Start Date", ""), "%Y-%m-%d").date()
                except:
                    st.session_state["start_date"] = datetime.now().date()
                try:
                    st.session_state["training_date"] = datetime.strptime(record.get("Training Date", ""), "%Y-%m-%d").date()
                except:
                    st.session_state["training_date"] = datetime.now().date()
                try:
                    st.session_state["complete_date"] = datetime.strptime(record.get("Complete Date", ""), "%Y-%m-%d").date()
                except:
                    st.session_state["complete_date"] = datetime.now().date()
                st.session_state["job_assigned"] = record.get("Job Assigned", "")
                
                # Update button
                if st.button("Update Implementation Record", use_container_width=True):
                    # Collect updated form data
                    updated_data = collect_implementation_form_data()
                    
                    # Update record in database
                    df = update_record(st.session_state.selected_implementation_record, updated_data)
                    st.success(f"✅ Implementation record for {updated_data['Company Name']} updated successfully!")
                    time.sleep(1)
                    st.session_state.edit_implementation_mode = False
                    st.session_state.selected_implementation_record = None
                    st.rerun()
                
                # Cancel button
                if st.button("Cancel Edit", use_container_width=True):
                    st.session_state.edit_implementation_mode = False
                    st.session_state.selected_implementation_record = None
                    st.rerun()