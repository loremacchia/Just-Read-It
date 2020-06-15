import requests
import os
print(os.getcwd())
url = "http://STRING.ngrok.io"
files = {'file': open('4.jpg', 'rb')}
requests.post(url, files=files)