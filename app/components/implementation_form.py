import streamlit as st

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
    
        # st.divider()
    
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
    
    # Submit Button
    if st.button("Submit Implementation Form", use_container_width=True):
        # Here you would add the logic to save the form data
        st.success("Implementation form submitted successfully!")