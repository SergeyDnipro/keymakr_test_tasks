from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
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
    task_title: str
    task_description: str
    status: bool = False

class UpdateTaskRecord(BaseModel):
    task_title: Optional[str] = None
    task_description: Optional[str] = None
    status: Optional[bool] = None


@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: TaskRecord):
    task_id = get_new_task_id()
    tasks[task_id] = task
    return {"id": task_id, "task": task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskRecord):
    validate_task_id(task_id)
    tasks[task_id] = task
    return {"id": task_id, "task": task}

@app.patch("/tasks/{task_id}")
def update_task_fields(task_id: int, update_fields: UpdateTaskRecord):
    validate_task_id(task_id)
    origin_task = tasks[task_id]
    updated_data = update_fields.model_dump(exclude_unset=True)
    tasks[task_id] = origin_task.model_copy(update=updated_data)
    return {"id": task_id, "task": tasks[task_id]}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    validate_task_id(task_id)
    deleted_task = tasks.pop(task_id)
    return {"id": task_id, "deleted_task": deleted_task}
