import requests
from bs4 import BeautifulSoup
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

def write_last_job(job_title):
    with open(LAST_JOB_FILE, "w") as f:
        f.write(job_title)

def check_job_post():
    url = "https://placements.codegnan.com/jobslist"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_table = soup.find('table', id='jobs')
    first_row = job_table.find('tbody').find('tr')
    cells = first_row.find_all('td')

    if not cells:
        print("No jobs found.")
        return

    job_title = cells[0].text.strip()
    company = cells[1].text.strip()
    location = cells[2].text.strip()

    last_job = read_last_job()
    if job_title != last_job:
        message = f"🧑‍💼 New Job Posted!\n\n📌 Title: {job_title}\n🏢 Company: {company}\n📍 Location: {location}"
        send_telegram_message(message)
        write_last_job(job_title)

check_job_post()
