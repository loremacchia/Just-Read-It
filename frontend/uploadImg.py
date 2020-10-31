import requests
import os
print(os.getcwd())
url = "http://38a21cb5e06c.ngrok.io "
files = {'image': open('text.png', 'rb')}
requests.post(url, files=files)