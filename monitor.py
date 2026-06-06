import requests
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email config
SENDER_EMAIL = "goyalriddhika13@gmail.com"
APP_PASSWORD = "qgqupfrfyvzfmotp"  # paste your app password here, remove spaces
RECEIVER_EMAIL = "goyalriddhika13@gmail.com"

services = [
    { "name": "Google", "url": "https://www.google.com" },
    { "name": "GitHub", "url": "https://www.github.com" },
    { "name": "JSONPlaceholder", "url": "https://jsonplaceholder.typicode.com" },
    { "name": "NASA API", "url": "https://api.nasa.gov" },
    { "name": "Fake Server 1", "url": "https://this-does-not-exist-123abc.com" },
    { "name": "Fake Server 2", "url": "https://dead-service-xyz987.io" },
]

def send_alert(service_name):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"🚨 ALERT: {service_name} is DOWN"

        body = f"""
        Cloud Monitor Alert

        Service: {service_name}
        Status: DOWN
        Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Automated alert from Cloud Infrastructure Monitor Dashboard.
        """
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"  >> Alert email sent for {service_name}")
    except Exception as e:
        print(f"  >> Email failed: {e}")

def check_service(service):
    try:
        response = requests.get(service["url"], timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {service['name']}: UP")
            return True
    except:
        pass
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {service['name']}: DOWN — sending alert")
    return False

def trigger_alert(service):
    with open("incident_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} — {service['name']} is DOWN. Alert sent.\n")
    send_alert(service["name"])

print("Python monitor started...")
while True:
    for service in services:
        is_up = check_service(service)
        if not is_up:
            trigger_alert(service)
    time.sleep(30)