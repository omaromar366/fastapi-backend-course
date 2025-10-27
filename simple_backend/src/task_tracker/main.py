from fastapi import FastAPI, HTTPException
from task_storage import GistStorage
from cloud_llm import CloudflareLLM
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel
from typing import List, Optional
from config import settings

app = FastAPI()
logger = logging.getLogger(__name__)

storage = GistStorage("https://api.github.com", settings.github_token)

llm = CloudflareLLM()


class TaskCreate(BaseModel):
    task_name: str


class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    status: Optional[str] = None


class Task(BaseModel):
    id: int
    task_name: str
    status: str
    solution: Optional[str] = None


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Необработанная ошибка: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"},
    )


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.load_data()


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(body: TaskCreate):
    tasks = storage.load_data()
    new_id = max([t.get("id", 0) for t in tasks], default=0) + 1
    solution = llm.get_solution(body.task_name)
    new_task = {"id": new_id, "task_name": body.task_name, "status": "in work", "solution": solution}
    tasks.append(new_task)
    storage.save_data(tasks)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, body: TaskUpdate):
    tasks = storage.load_data()
    for task in tasks:
        if task["id"] == task_id:
            if body.task_name is not None:
                task["task_name"] = body.task_name
            if body.status is not None:
                task["status"] = body.status
            storage.save_data(tasks)
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    tasks = storage.load_data()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            storage.save_data(tasks)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
