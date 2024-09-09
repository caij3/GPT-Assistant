# Get ngrok url request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# Replace this URL with your ngrok URL
ngrok_url = os.environ["NGROK_URL"]
print(ngrok_url)

# Send GET request
response = requests.get(ngrok_url)

# Print response
print(response.json())
