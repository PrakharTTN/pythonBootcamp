'''Q1. Write an object oriented code in Python, to download Gmail with attachments .

Create a "Emails.json"  file

In  "Emails.json"  file,  using Python `pickle`  module, dump following information:

- subject
- date
- from email
- number of words and line in email body
- number of attachments
- name of attachments

Each like in "Email.json" should be a valid JSON
'''

import yaml
import imaplib
import email
import pickle
import json
from email.header import decode_header

class EmailEnvironment:

    def __init__(self):
        self.user=""
        self.passw=""
        self.session= None
        self.emails=[]
    
    #This function dumps the details from emails[] into JSON files.
    def dump(self):
        with open("Email.json","w") as file, open("EmailPickle.json",'wb') as file2:
                print(self.emails)
                json.dump(self.emails,file,indent=4)
                pickle.dump(self.emails,file2)
    
    #This function loads the config.yaml file and safe loads and parses the username and password
    def loading_creds(self,filepath):
            with open(filepath,'r') as creds:
                credentials=yaml.safe_load(creds)
                self.user=credentials['user']
                self.passw=credentials['password']
                print("Successfully read the config file with credentials.")
                self.connection()
            # print("Failed to load credentials.")
    
    #This function creates a session with my gmail account
    def connection(self):
        
            self.session =imaplib.IMAP4_SSL('imap.gmail.com')
            self.session.login(self.user,self.passw)
            print("Access has been granted. Fetching mail details.")
            self.fetch_emails()
            self.session.logout()



    #This function checks for attachments in the mail and 
    #Returns a list with names of emails and total number of attachments
    def get_attachments(self,msg):
        attachments=[]
        for part in msg.walk():
            content_disposition = part.get('Content-Disposition')
            if content_disposition and 'attachment' in content_disposition.lower():
                attachments.append(part.get_filename())
        if len(attachments)==0:
            return None,0        
        return attachments,len(attachments)
    
    #This function checks the body from the mail and returns total words and total lines
    def get_body(self,msg):
        body_length=0
        body_lines=0
        for part in msg.walk():
            # Get Body by checking if it is plain text
            if part.get_content_type() == "text/plain":
                # Decode the body
                body = part.get_payload(decode=True).decode()
                body_lines=body.count('\n')
                body_length=len(body.split()) 
        return body_length,body_lines

    # Fetch all emails from inbox
    def fetch_emails(self):
        max_emails=5 #Specified total emails I want to download
        self.session.select("inbox")
        status, messages = self.session.search(None, "ALL") 
        email_ids = messages[0].split()[-max_emails:]

        for email_id in email_ids:
            # Fetch each email
            status, data = self.session.fetch(email_id, "(RFC822)")
            for response in data:
                if type(response) is tuple:

                    #Response[0] is the header file, while [1] is the main body
                    msg = email.message_from_bytes(response[1]) 

                    #Decodes the subject header
                    subject = decode_header(msg["subject"])[0][0]  
                    date = msg["date"]
                    sender = msg["from"]
                    body_length,body_lines = self.get_body(msg)
                    attachment, total_attachments = self.get_attachments(msg)
                    self.emails.append({
                        "subject": subject,
                        "date": date,
                        "from": sender,
                        "total_words": body_length,
                        "total_lines": body_lines,
                        "total_attachments":total_attachments,
                        "attachment": attachment
                    })
                    #Call the dump function to dump
        self.dump()
        print("Dumped the data in JSON files. Check directory.")


#Specified path of my config
path="/home/prakhar/Desktop/config.yaml"
a=emailEnvironment()
a.loading_creds(path)   