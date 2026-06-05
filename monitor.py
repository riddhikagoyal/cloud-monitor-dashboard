import requests
import time
import subprocess
import datetime

# Services to monitor
services = [
    { "name": "Google", "url": "https://www.google.com" },
    { "name": "GitHub", "url": "https://www.github.com" },
    { "name": "JSONPlaceholder", "url": "https://jsonplaceholder.typicode.com" },
]

def check_service(service):
    try:
        response = requests.get(service["url"], timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {service['name']}: UP")
            return True
    except:
        pass
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {service['name']}: DOWN — triggering alert")
    return False

def trigger_alert(service):
    # Logs the incident to a file — simulates incident response
    with open("incident_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} — {service['name']} is DOWN. Auto-restart triggered.\n")
    print(f"  >> Incident logged for {service['name']}")

# Poll every 30 seconds
print("Python monitor started...")
while True:
    for service in services:
        is_up = check_service(service)
        if not is_up:
            trigger_alert(service)
    time.sleep(30)
