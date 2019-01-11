import requests
import os

from requests.adapters import HTTPAdapter

model = os.getenv("model")
image_version = os.getenv("image_version")
frame = os.getenv("frame")
log_name = os.getenv("log_name")
host_endpoints = ""
url = "http://{3}/{0}/{1}/{2}".format(frame, image_version, model, host_endpoints)
print(url)
data = None
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
file_name = '/home/crim/%s' % log_name
if os.path.exists(file_name):
    files = {'file': open(file_name, 'rb')}
else:
    files = {'file': open('./%s' % log_name, 'rb')}
r = s.post(url, data, files=files)
s.close()
