import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
from Config import conn_str
from Outlook import *

def Issue_Category():
    
    option = ''
    st.title('Issues Categorization')

    # Establish a connection
    conn = pyodbc.connect(conn_str)

    query_datewiseSeparation = """
        select format([Email received Date],'dd/MM') as [Email received Date],[Issues Category] ,count(*) as [Count]
        from EmailsInfo 
        group by [Issues Category],[Email received Date]
        """

    data_datewiseSeparation = pd.read_sql(query_datewiseSeparation, conn)
    st.dataframe(data_datewiseSeparation)
    st.text('')
    st.line_chart(data_datewiseSeparation, y = 'Count', x = 'Email received Date', height = 300)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Error Login To Continue")
else:
    Issue_Category()                                        
