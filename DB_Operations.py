import pyodbc
import datetime
from Config import conn_str

def insertDataToDB(emailFrom,emailTo,emailCC,emailSub,emailBody,emailSummary,issuesCategory,emailReceivedDate,sentiment_result):
    conn = pyodbc.connect(conn_str)

    # Insert Query
    query = """insert into EmailsInfo
            ([Email From],[Email To],[Email CC],[Email Subject],[Email Body],[Email Body Summary],[Email received Date],[Issues Category],[Sentiment Analysis],[Data Entry Date])
            values (?,?,?,?,?,?,?,?,?,?)
            """
    # Update Query
    update_query = """
                    update	EmailsInfo
                    set		[ID] = left(a.[Issues Category],4) +'_'+convert(varchar,convert(date,a.[Email received Date]),112) +'-'+ convert(varchar,count_val)
                    from	EmailsInfo a
                    inner join
                    (
                    select	[Issues Category],[Email received Date], count(*) as count_val 
                    from	EmailsInfo 
                    group by	[Issues Category], [Email received Date]
                    )b
                    on		a.[Issues Category] = b.[Issues Category]
                    and		a.[Email received Date] = b.[Email received Date]
                    where	[ID] is null
                   """
    # Create a cursor object
    cursor = conn.cursor()

    # Use datetime.now() to get the current date and time
    current_date_time = datetime.datetime.now()
    
    # Execute the insert query
    cursor.execute(query,(emailFrom,emailTo,emailCC,emailSub,emailBody,emailSummary,emailReceivedDate,issuesCategory,sentiment_result,current_date_time))
    conn.commit()

    # Execute the update query for generating ticket ID
    cursor.execute(update_query)
    conn.commit()

    # Select Ticket ID query
    select_Ticket_ID_query = 'select top(1)[ID] from EmailsInfo where [Email Sent Flag] is null order by [Sr. No] Desc'

    # Execute the query
    cursor.execute(select_Ticket_ID_query)

    # Fetch the results
    rows = cursor.fetchall()

    # Convert the results to a list of dictionaries
    ticket_ID = rows[0][0]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return ticket_ID

def updateStatus(ticket_ID):
    conn = pyodbc.connect(conn_str)

    update_query = "update EmailsInfo set [Email Sent Flag] = 'True', [Ticket Status] = 'Open' where ID = ?"

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the update query for setting flag for email sent status
    cursor.execute(update_query,(ticket_ID))
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def fetchLoginDetails(username):
    conn = pyodbc.connect(conn_str)

    # Select Ticket ID query
    select_LoginDetails = 'select [Password] from [Login Info] where UserName = ?'

    # Create a cursor object
    cursor = conn.cursor()

    try:
        # Execute the query
        cursor.execute(select_LoginDetails,username)

        # Fetch the results
        rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        password = rows[0][0]
    except:
        password = "Error"

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return password

def fetchTicketStatus(ticketID):
    conn = pyodbc.connect(conn_str)

    # Select Ticket ID query
    select_TicketStatus = 'select [Ticket Status] from EmailsInfo where ID = ?'

    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute(select_TicketStatus,ticketID)

    try:
        # Fetch the results
        rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        status = rows[0][0]
    except:
        status = "Error"

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return status

def updateTicketStatus(ticketID,status,username):
    conn = pyodbc.connect(conn_str)

    # Select Ticket ID query
    update_TicketStatus = f"update EmailsInfo set [Ticket Status] = '{status}', [Modified By] = '{username}' where ID = '{ticketID}'"

    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute(update_TicketStatus)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
