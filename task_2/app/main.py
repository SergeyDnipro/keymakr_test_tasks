from fastapi import FastAPI
from celery_tasks import csv_task

app = FastAPI()

@app.get("/")
def start_page():
    return {"msg": "fetch data every 1 minute"}

@app.get("/fetch")
def fetch():
    task = csv_task.delay(autostart=False)
    return {"task id": task.id, "status": task.status}