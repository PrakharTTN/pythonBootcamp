import requests
from requests.exceptions import *
import json

class RequestHandling:
   
    def get(self, url, header, timeout=10, payload=None):
        '''Implements the Get the function'''
        try:
            response = requests.get(url, headers=header, params = payload, timeout=timeout)
            response.raise_for_status() 
            return response.json
            
        except requests.exceptions.InvalidHeader as error:
            print("Invalid Header Provided.")

        except requests.exceptions.HTTPError as error:
            print("HTTP error found. \n", self.HTTP_error(response.status_code))
        
        except requests.exceptions.ConnectionError as error:
            print("Connection error found: ")
        
        except requests.exceptions.Timeout as error:
            print("Connection Timedout: ")
        
        except requests.exceptions.RequestException as error:
            print("Other Error: ")

        except requests.exceptions.TooManyRedirects as error:
            print("Too many redirects from server: ")

    def http_error(self, error_code):
        '''This block is to return respective HTTP error.'''
        error_dict = {
            404: "Error 404: Resource not found",
            500: "Error 500: Internal server error",
            503: "Error 503: Service unavailable",
            401: "Error 401: Unauthorized",
            403: "Error 403: Forbidden",
        }
        return error_dict.get(error_code)

request_object= RequestHandling()
get_json= request_object.get(url="http://www.google.com",header={},timeout=10)

if get_json:
    print("Success:", json.dumps(get_json,indent=4))
else:
    print("No content.")
