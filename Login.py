from DB_Operations import fetchLoginDetails
from Outlook import *
import streamlit as st

if 'UserName' not in st.session_state:
    st.session_state.UserName = ''

def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    passwd = st.text_input("Password", type="password")

    #st.button("Execute Script", onclick = outlookMailsRead())

    #st.button("Login", onclick = auth(username,passwd))

    if st.button("Login"):
        if username != '':
            PASSWORD = fetchLoginDetails(username)
            if passwd == PASSWORD:
                st.success("Logged in as {}".format(username))
                st.session_state.logged_in = True
                st.session_state.UserName = username
            else:
                st.error("Invalid username or password")
        else:
            st.error("Username is Blank")


def main():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page()

if __name__ == "__main__":
    main()
