'''Q2. In download email assignment,

Provision to download only selective email. For example:

- To download only emails which have attachments
- To download only email which are related to Job
- To download only the email which have picture attached

'''

import yaml
import imaplib
import email
import pickle
import json
from email.header import decode_header
import argparse

class emailEnvironment:

    def __init__(self):
        self.user=""
        self.passw=""
        self.session= None
        self.emails=[]
        self.flag=0
    
    #This function dumps the details from emails[] into JSON files.
    def dump(self):
        with open("Email.json","w") as file, open("EmailPickle.json",'wb') as file2:
            json.dump(self.emails,file,indent=2)
            pickle.dump(self.emails,file2)
    
    #This function loads the config.yaml file and safe loads and parses the username and password
    def loading_creds(self,filepath, flag):
        # try:
            with open(filepath,'r') as creds:
                credentials=yaml.safe_load(creds)
                self.user=credentials['user']
                self.passw=credentials['password']
                print("Successfully read the config file with credentials.")
                self.flag=flag
                self.connection()
        # except Exception as e:
            # print("Failed to load credentials.")
    
    #This function creates a session with my gmail account
    def connection(self):
        # try:
            self.session =imaplib.IMAP4_SSL('imap.gmail.com')
            self.session.login(self.user,self.passw)
            print("Access has been granted. Fetching mail details.")
            self.fetch_emails()
        # except Exception as e:
        #     print("Failed to connect, check email/password. ")

    #This function checks for attachments in the mail and 
    #Returns a list with names of emails and total number of attachments
    def get_attachments(self,msg):
        attachments=[]
        #If attachment is image, return true
        hasImage=False
        for part in msg.walk():
            content_disposition = part.get('Content-Disposition')
            if part.get_content_type().startswith('image/'):
                hasImage=True
            if content_disposition and 'attachment' in content_disposition.lower():
                attachments.append(part.get_filename())
        if len(attachments)==0:
            return None,0,hasImage        
        return attachments,len(attachments),hasImage
    
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
        #Specified total emails I want to download
        maxemails=5
        self.session.select("inbox")
        status, messages = self.session.search(None, "ALL") 
        email_ids = messages[0].split()[-maxemails:]

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
                    attachment, total_attachments, hasImage= self.get_attachments(msg)

                    #Created conditional casing to ignore when the case matches and provision is false

                    #In this flag is 1 which is mails w/ attachments
                    #However if attachments is 0, it will not append to final list
                    if self.flag==1 and total_attachments==0:
                        continue

                    #In this flag is 2 which is Job emails
                    #However if sender's mail will not have domain, it will not append
                    elif self.flag==2 and '@tothenew.com' not in sender:
                        continue

                    #In this flag is 3, which mails with images, in the hasImage variable
                    #has been passed from attachment functions, which is true if the mail has image
                    #Providing if hasImage is false, it will not append
                    elif self.flag == 3 and  not hasImage:
                        continue
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
                    try:
                        self.dump()
                    except Exception as e:
                        print("Couldn't dump, check files. ")
        print("Dumped the data in JSON files. Check directory.")

#Specified path of my config
path="/home/prakhar/Desktop/config.yaml"
a=emailEnvironment()

#Match case to provide provisions
#1. To download only emails which have attachments
#2. To download only email which are related to Job
#3. To download only the email which have picture attached

parser=argparse.ArgumentParser("This is to parse provisions to downloader.")
print("1. To download Emails with Attachments \n2. To download only email which are related to Job\n3. To download only the email which have picture attached")
n=int(input("Enter the case: "))
match n:
    case 1:
        a.loading_creds(path,flag=1)
    case 2:
        a.loading_creds(path,flag=2)
    case 3:
        a.loading_creds(path,flag=3)






