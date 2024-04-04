import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
from Config import conn_str
from Outlook import *
from DB_Operations import *

if 'clicked' not in st.session_state:
    st.session_state.clicked = 0

def click_button_Open():
    st.session_state.clicked = 1
def click_button_Close():
    st.session_state.clicked = 2
        

def Admin_Page():
    
    option = ''
    st.title('Admin Page')

    if st.button("Execute Backend Code", help = "Run the main backend code for Emails check"):
        outlookMailsRead()        

    # Establish a connection
    conn = pyodbc.connect(conn_str)

    #Select data parameters
    options = st.multiselect(
        'Modify below datatable columns',
        ('Email Subject','Email Body','Data Entry Date','Email Body Summary','Sentiment Analysis','Email Sent Flag','Approval status','Modified By'))

    for item in options:
        option += ',[' + item + ']'

    # Example query
    query = f'select [Email From],[ID],[Issues Category],[Email received Date],[Ticket Status]{option} from EmailsInfo order by [Email received Date] desc'

    # Load 10,000 rows of data into the dataframe from SQL
    data_load_state = st.text('Loading data...')
    data = pd.read_sql(query, conn)
    data_load_state.text('')
    st.dataframe(data)

    st.title("Modify Ticket Status")
    modify_ticketID = st.text_input("Enter Ticket ID to Modify")

    if st.button("Alter Status"):
        if modify_ticketID != '':
            status = fetchTicketStatus(modify_ticketID)
            if status == "Open":
                st.button("Close this Ticket", on_click = click_button_Open)
            elif status == "Closed":
                st.button("Re Open this Ticket", on_click = click_button_Close)
            elif status =="Error":
                st.error("Ticket ID Entered is Invalid")
        else:
            st.error("Please Enter Ticket ID")

    if st.session_state.clicked == 1:
        updateTicketStatus(modify_ticketID,"Closed",st.session_state.UserName)
        st.session_state.clicked = 0
    elif st.session_state.clicked == 2:
        updateTicketStatus(modify_ticketID,"Open",st.session_state.UserName)
        st.session_state.clicked = 0

    st.button("Reload")
    
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Error Login To Continue")
else:
    Admin_Page()
