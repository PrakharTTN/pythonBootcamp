import requests
from requests.exceptions import *

class exceptions:
    timeoutError="Timeout Error: Request timed out."
    badRequest="Error badRequest"
class requestHandling:
    def __init__(self, url):
        self.url = url
    def get(self,payload=None):
        try:
            response = requests.get(self.url,params=payload,timeout=10)
            response.raise_for_status() 
            return response
        except requests.exceptions.HTTPError as error:
            print("HTTP error found:", error)
        except requests.exceptions.ConnectionError as error:
            print("Connection error found: ",error)
        except requests.exceptions.Timeout as error:
            print("Connection Timedout: ",error)
        except requests.exceptions.RequestException as error:
            print("Other Error: ", error)
        except requests.exceptions.TooManyRedirects as error:
            print("Too many redirects from server: ",error)

singlerequest = requestHandling("http://www.google.com")
final = singlerequest.get()

if final:
    print("Success:", final)
else:
    print("Failed to retrieve content.")
