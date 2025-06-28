import requests
import os
from datetime import datetime, timedelta

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
LAST_JOB_FILE = "last_job.txt"
LAST_NO_JOB_PING = "last_ping.txt"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def read_file(filename):
    if not os.path.exists(filename):
        return ""
    with open(filename, "r") as f:
        return f.read().strip()

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def should_send_no_job_ping():
    last_ping = read_file(LAST_NO_JOB_PING)
    if not last_ping:
        return True
    try:
        last_time = datetime.strptime(last_ping, "%Y-%m-%d")
        return datetime.now() - last_time >= timedelta(days=1)
    except:
        return True

def check_job_post():
    url = "https://placements.codegnan.com/api/jobposts/getAllJobs"
    headers = {
        "User-Agent": "JobAlertBot/1.0 (Personal use by student for job updates)"
    }

    response = requests.get(url, headers=headers)

    try:
        jobs = response.json()
    except Exception as e:
        print("Failed to decode JSON. Response text:")
        print(response.text)
        return

    if not jobs:
        print("No jobs found.")
        return

    latest = jobs[0]
    job_id = str(latest['id'])
    title = latest['title']
    company = latest['companyName']
    location = latest['location']

    last_id = read_file(LAST_JOB_FILE)

    if job_id != last_id:
        message = f"🧑‍💼 New Job Posted!\n\n📌 Title: {title}\n🏢 Company: {company}\n📍 Location: {location}"
        send_telegram_message(message)
        write_file(LAST_JOB_FILE, job_id)
        write_file(LAST_NO_JOB_PING, datetime.now().strftime("%Y-%m-%d"))
    else:
        if should_send_no_job_ping():
            send_telegram_message("🤖 No new jobs posted yet. I'm still watching!")
            write_file(LAST_NO_JOB_PING, datetime.now().strftime("%Y-%m-%d"))
        else:
            print("No new job and no need to send ping today.")

check_job_post()


