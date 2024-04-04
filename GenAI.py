from openai import OpenAI

def gen_Data(emailFrom,emailTo,emailCC,emailSub,email_body,emailReceivedDate):
    client = OpenAI()

    # Define a basic prompt
    prompt_Categorization = "You are a workflow/helpdesk classifier.Technical issue: I'm experiencing a technical issue with your product, Billing Inquiry:I have a question about my billing statement, Feature Request:I'd like to suggest a new feature for your product, General Inquiry:Can you provide information about your services. Generate a classification to the following prompt in words and not a sentence"
    prompt_Summary = "I need you to give me a brief summary for the following Email Body max 10-15 words."
    prompt_Sentiment = "Analyse the following sentence and provide me a sentiment analysis for the same in a single word: Positive,Negative or Neutral"

    # For Categorization
    completion_Categorization = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=[
        {"role": "system", "content": prompt_Categorization},
        {"role": "user", "content": email_body}
      ]
    )

    # For Mail Summary
    completion_Summary = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=[
        {"role": "system", "content": prompt_Summary},
        {"role": "user", "content": email_body}
      ]
    )

    # For Sentiment Analysis
    completion_Sentiment = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=[
        {"role": "system", "content": prompt_Sentiment},
        {"role": "user", "content": email_body}
      ]
    )

    client.close()
    
    issuesCategory = completion_Categorization.choices[0].message.content
    emailSummary = completion_Summary.choices[0].message.content
    sentiment_result = completion_Sentiment.choices[0].message.content

    #ticket_ID = insertDataToDB(emailFrom,emailTo,emailCC,emailSub,email_body,emailSummary,issuesCategory,emailReceivedDate,sentiment_result)

    return issuesCategory, emailSummary, sentiment_result

def GenAI_Reply_Email(sentiment_result, ticket_ID, emailFrom, emailSummary):
    client = OpenAI()

    # Define a basic prompt
    prompt_ReplyEmail = """I will provide you with email sentiment, ticket ID, email summary, on that basis,
                            I want you to write a email body that replies to that email acknowledgment that the ticket has been raised with the ticket number
                            and whereve possible, write basic troubleshooting steps, also don't write the subject and keep signature as Best Regards, IT Helpdesk."""

    user_Content = f'Sentiment : {sentiment_result}, Ticket ID : {ticket_ID}, Name : {emailFrom}, Summary : {emailSummary}.'
    # For Categorization
    completion_ReplyEmail = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=[
        {"role": "system", "content": prompt_ReplyEmail},
        {"role": "user", "content": user_Content}
      ]
    )
    return completion_ReplyEmail.choices[0].message.content
