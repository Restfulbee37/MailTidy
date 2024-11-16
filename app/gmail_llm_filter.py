import imaplib
import email
from email.header import decode_header
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Your email credentials from environment variables
username = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

if not username or not password:
    raise ValueError("Email address and password must be set in environment variables.")

# Function to move email to a specific folder
def move_email_to_folder(mail, email_id, folder_name):
    mail.copy(email_id, folder_name)
    mail.store(email_id, '+FLAGS', '\\Deleted')
    mail.expunge()

# Function to classify the email via LLM API
def classify_email_via_llm(subject, body):
    url = "http://localhost:11434/api/generate"
    
    # Construct the prompt
    prompt_template = """
    You are an AI trained to classify emails. Please read the email content below and classify it into one of the following categories: 'spam', 'important', or 'regular'. Your response should only be one word.
    
    Be particularly vigilant about identifying 'spam'. Spam emails often include characteristics like:
    - Marketing emails promoting sales, discounts, or special offers
    - Unsolicited advertisements or promotions
    - Newsletters or content related to product launches, events, or entertainment
    - Emails trying to sell products, services, or subscriptions
    - Offers or deals such as 40% off
    - We've got you covered deals 
    
    Example of spam:
    Subject: "Easter Holiday is almost here! Get all EGGcited with our Easter holiday special: 4shared Premium Account 30% OFF!"
    Body: "May the spirit of Easter fill your heart with complete joy and peace. The coupon is valid till 1 May 2014."

    Example of spam:
    Subject: "New and Amazing Assetto Corsa Mods"
    Body: "We have a serious new batch of Assetto Corsa content in different categories."

    Example of spam:
    Subject: "In Cinemas Now"
    Body: "Get ready to see Zendaya like never before; experience Challengers in cinemas NOW!"

    Example of important:
    Subject: "Invoice for your recent purchase"
    Body: "Please find attached the invoice for your recent purchase."

    Example of regular:
    Subject: "Team meeting rescheduled"
    Body: "The team meeting has been rescheduled to next Monday."
    
    Now, classify the following email:
    
    Email Content:
    Subject: {subject}
    
    {body}
    
    Your classification:
    """
    
    # Format the prompt with the email subject and body
    prompt = prompt_template.format(subject=subject, body=body)
    
    # Send the request to the LLM API
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Parse the JSON response
        result = response.json()
        llm_output = result.get("response", "").strip().lower()  # Strip whitespace and make lowercase
        
        # Determine the label based on LLM output
        if "spam" in llm_output:
            return "spam"
        elif "important" in llm_output:
            return "important"
        else:
            return "regular"
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LLM API: {e}")
        return "regular"  # Default to "regular" on failure

# Connect to the Gmail IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Login to your account
mail.login(username, password)

# Select the mailbox you want to check (e.g., "inbox")
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# Process each email
for email_id in email_ids:
    # Fetch the email by ID
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            
            # Handle missing subject
            subject_header = msg["Subject"]
            if subject_header is None:
                subject = "No Subject"
            else:
                subject, encoding = decode_header(subject_header)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
            
            # Decode the email body
            if msg.is_multipart():
                # If the email has multiple parts
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        email_body = part.get_payload(decode=True)
                        # Try to decode with UTF-8, fallback if it fails
                        try:
                            email_body = email_body.decode()
                        except UnicodeDecodeError:
                            # If UTF-8 fails, try ISO-8859-1 or other encodings
                            email_body = email_body.decode('ISO-8859-1')
                        break
            else:
                # For emails with a single part
                email_body = msg.get_payload(decode=True)
                try:
                    email_body = email_body.decode()
                except UnicodeDecodeError:
                    email_body = email_body.decode('ISO-8859-1')
            
            # Classify the email using LLM
            label = classify_email_via_llm(subject, email_body)
            
            # Move the email based on the LLM's classification
            if label == "spam":
                move_email_to_folder(mail, email_id, "s")
                print(f"Moved to 's': {subject}")
            elif label == "important":
                move_email_to_folder(mail, email_id, "i")
                print(f"Moved to 'i': {subject}")
            else:
                print(f"Kept in inbox: {subject}")


# Logout from the server
mail.logout()

