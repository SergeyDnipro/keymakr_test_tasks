from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from itertools import count


app = FastAPI()
task_id_counter = count(1)
tasks: Dict[int, "TaskRecord"] = {}


def get_new_task_id():
    return next(task_id_counter)

def validate_task_id(task_id):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")


class TaskRecord(BaseModel):
    id: int | None = None
    task_title: str
    task_description: str
    status: bool = False


@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: TaskRecord):
    task.id = get_new_task_id()
    tasks[task.id] = task
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskRecord):
    validate_task_id(task_id)
    tasks[task_id] = task
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    validate_task_id(task_id)
    deleted_task = tasks.pop(task_id)
    return {"task_id": deleted_task.id, "deleted_task": deleted_task}