import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please Log In to Continue")
else:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success("Logout Successful")
