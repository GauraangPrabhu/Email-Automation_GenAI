import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
from Config import conn_str
from Outlook import *

def Ticket_Status():
    
    option = ''
    st.title('Tickets Information')
    if st.button('Log Out'):
        conn.close()
        for key in st.session_state.keys():
            del st.session_state[key]

    # Establish a connection
    conn = pyodbc.connect(conn_str)

    query_TicketStatusCount = "select [Ticket Status],count(*) as [Count] from EmailsInfo group by [Ticket Status]"
    data_TicketStatusCount = pd.read_sql(query_TicketStatusCount, conn)
    st.dataframe(data_TicketStatusCount)

            
    if st.button('Execute Backend Code',help='Run Main Code Backend'):
        outlookMailsRead()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Error Login To Continue")
else:
    Ticket_Status()
