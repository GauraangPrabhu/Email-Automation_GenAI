import win32com.client
import re
from DB_Operations import *
from GenAI import *
import time

def outlookMailsRead():
    
    # Open An Outlook Session
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    time.sleep(5)

    #Point to Inbox folder
    inbox = outlook.GetDefaultFolder(6) # "6" = Inbox Folder

    #Get Unread Messages
    unread_messages = inbox.Items.Restrict("[Unread] = true")

    for message in unread_messages:
        #print('found unread')

        # Retrieve recipients (To)
        to_recipients = "; ".join([recipient.Name for recipient in message.Recipients if recipient.Type == 1])

        # Retrieve recipients (CC)
        cc_recipients = "; ".join([recipient.Name for recipient in message.Recipients if recipient.Type == 2])

        #Email Body
        email_body = message.Body
        # For removing links betwween '<', '>' 
        pattern = r'<.*?>'
        email_body = re.sub(pattern, '', email_body)
        # Remove newline characters
        email_body = email_body.replace('\n', '').replace('\r', '').replace("’","").replace("'","")
        # Trim leading and trailing whitespaces
        email_body = email_body.strip()
        # Mark the email as read
        message.UnRead = False

        # Gen AI Function
        issuesCategory, emailSummary, sentiment_result = gen_Data(message.SenderName,to_recipients,cc_recipients,message.Subject,email_body,message.ReceivedTime)
        print("Email Summary = ",emailSummary)

        #Insert Data to DB
        ticket_ID = insertDataToDB(message.SenderName,to_recipients,cc_recipients,message.Subject,email_body,emailSummary,issuesCategory,message.ReceivedTime,sentiment_result)
        print("ID = ",ticket_ID)

        #Generate Reply for Email
        reply_body = GenAI_Reply_Email(sentiment_result, ticket_ID, message.SenderName, emailSummary)

        # Send Reply for the email
        reply_email = message.Reply()
        reply_email.Body = reply_body

        # Send the reply
        reply_email.Send()

        # Update status in DB afer Email is triggered
        updateStatus(ticket_ID)

        time.sleep(5)
        
    # Close An Outlook Session
    
    outlook.Application.Quit()


outlookMailsRead()
