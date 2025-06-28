import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
LAST_JOB_FILE = "last_job.txt"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def read_last_job():
    if not os.path.exists(LAST_JOB_FILE):
        return ""
    with open(LAST_JOB_FILE, "r") as f:
        return f.read().strip()

def write_last_job(job_id):
    with open(LAST_JOB_FILE, "w") as f:
        f.write(job_id)

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
    job_id = str(latest['id'])  # Unique job ID
    title = latest['title']
    company = latest['companyName']
    location = latest['location']

    last_id = read_last_job()
    if job_id != last_id:
        message = f"🧑‍💼 New Job Posted!\n\n📌 Title: {title}\n🏢 Company: {company}\n📍 Location: {location}"
        send_telegram_message(message)
        write_last_job(job_id)
    else:
        print("No new job found.")

check_job_post()

