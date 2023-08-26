import requests
from bs4 import BeautifulSoup

def validate_aadhaar(aadhaar_number):
   # Create a session to maintain cookies
   session = requests.Session()

   # Make an initial GET request to the UIDAI's Aadhaar validation page to get cookies
   response = session.get("https://resident.uidai.gov.in/verify")

   # Parse the response content
   soup = BeautifulSoup(response.content, "html.parser")

   # Find the CSRF token if it exists
   csrf_token_input = soup.find("input", {"name": "csrf_token"})
   if csrf_token_input:
       csrf_token = csrf_token_input["value"]
   else:
       print("CSRF token not found.")
       return False

   # Prepare the data for POST request
   data = {
       "uidNumber": aadhaar_number,
       "csrf_token": csrf_token,
       "option": "checkotp"
   }

   # Send the POST request to validate the Aadhaar number
   response = session.post("https://resident.uidai.gov.in/verify", data=data)

   # Check the response for validation
   if "otp_verification is done" in response.text:
       return True
   else:
       return False

# Test the function
aadhaar_number = "3107-6585-4562"  # Replace with the Aadhaar number you want to verify
if validate_aadhaar(aadhaar_number):
   print("Valid Aadhaar Number")
else:
   print("Invalid Aadhaar Number")
