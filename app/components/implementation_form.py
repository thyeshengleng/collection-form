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
    
    # Submit Button
    if st.button("Submit Implementation Form", use_container_width=True):
        # Here you would add the logic to save the form data
        st.success("Implementation form submitted successfully!")