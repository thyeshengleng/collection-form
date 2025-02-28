import streamlit as st

def render_implementation_form():
    # Company Information
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("COMPANY NAME")
        module = st.text_input("AUTOCOUNT MODULE")
        start_date = st.date_input("ACTUAL START DATE")
    with col2:
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
        (3, "ZEROTIER / RADMIN"),
        (4, "SQL SERVER"),
        (5, "LICENSE ACTIVATION")
    ]
    
    for step, desc in installation_steps:
        cols = st.columns([1, 4, 2, 2, 2])
        with cols[0]:
            st.write(step)
        with cols[1]:
            st.write(desc)
        with cols[2]:
            version = st.text_input("", key=f"version_{step}")
        with cols[3]:
            status = st.selectbox(
                "",
                ["PENDING", "ERROR", "DONE"],
                key=f"status_{step}"
            )
        with cols[4]:
            date = st.date_input("", key=f"date_{step}")

    
    st.markdown("#### IMPLEMENTATION:")
    
    # Implementation steps
    implementation_steps = [
        (6, "DATABASE INSTANT NAME"),
        (7, "SETUP COMPANY PROFILE / LOGO / HEADER"),
        (8, "SETUP CHART OF ACCOUNT")
    ]
    
    for step, desc in implementation_steps:
        cols = st.columns([1, 4, 2, 2, 2])
        with cols[0]:
            st.write(step)
        with cols[1]:
            st.write(desc)
        with cols[2]:
            version = st.text_input("", key=f"version_{step}")
        with cols[3]:
            status = st.selectbox(
                "",
                ["PENDING", "ERROR", "DONE"],
                key=f"status_{step}"
            )
        with cols[4]:
            date = st.date_input("", key=f"date_{step}")
    
    # Submit Button
    if st.button("Submit Implementation Form", use_container_width=True):
        # Here you would add the logic to save the form data
        st.success("Implementation form submitted successfully!")