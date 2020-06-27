import requests
import os
print(os.getcwd())
url = "http://deaec689aef6.ngrok.io"
files = {'image': open('index.png', 'rb')}
requests.post(url, files=files)