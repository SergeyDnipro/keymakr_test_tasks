import requests
import csv
from pathlib import Path
from celery import Celery
from logger_conf import logger_decorator
from celery.schedules import crontab


app = Celery(
    'csv_task',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
)

DATA_FILE = Path(__file__).parent.parent / 'data/output.csv'
API_URL = "https://jsonplaceholder.typicode.com/users"
FIELDS = ['id', 'name', 'email']


app.conf.beat_schedule = {
    'auto-fetch-data': {
        'task': 'celery_tasks.csv_task',
        'schedule': crontab(minute="*/1"),
    }
}

@app.task
@logger_decorator
def csv_task(*, autostart: bool=True):
    """ Delayed task to fetch, check and save data to 'csv' file """

    # Fetch data from url
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    current_ids = set()

    file_exist = DATA_FILE.exists()
    autostart_msg = '[AUTO]' if autostart else '[MANUAL]'

    # Collect all ID's in the existing 'csv' file
    if file_exist:
        with open(DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            file_dataset = csv.DictReader(csvfile)
            current_ids = {row["id"] for row in file_dataset}

    # Create new dataset, comparing new and existing ID's
    new_records = [row for row in data if str(row["id"]) not in current_ids]

    if not new_records:
        return f"{autostart_msg} No new records"

    # Write filtered distinct data in 'csv' file
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)

        if not file_exist:
            writer.writeheader()

        for row in new_records:
            filtered_record = {key: row[key] for key in row if key in FIELDS}
            writer.writerow(filtered_record)

        return f"{autostart_msg} Records fetched and saved successfully"
