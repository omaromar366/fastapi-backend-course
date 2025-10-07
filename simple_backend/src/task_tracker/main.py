from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

DATA_FILE = 'tasks.json'


class TaskStorage:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecoderError:
                    return []
        return []

    def save(self, tasks):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)


class TasksManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load()
        self.next_id = self._get_next_id()

    def _get_next_id(self):
        return max([t['id'] for t in self.tasks], default=0) + 1

    def get_tasks(self):
        return self.tasks

    def create_task(self, task_name: str):
        if not task_name.strip():
            raise HTTPException(status_code=400, detail="Task name cannot be empty")

        task = {'id': self.next_id, 'task_name': task_name, 'status': 'In Work'}
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save(self.tasks)
        return task

    def update_task(self, task_id: int, task_name: str = None, status: str = None):
        for task in self.tasks:
            if task['id'] == task_id:
                if task_name:
                    task['task_name'] = task_name
                if status:
                    task['status'] = status
                self.storage.save(self.tasks)
                return task
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id: int):
        for task in self.tasks:
            if task['id'] == task_id:
                self.tasks.remove(task)
            self.storage.save(self.tasks)
            return {"message": "Task deleted"}
        raise HTTPException(status_code=404, detail="Task not found")


storage = TaskStorage(DATA_FILE)
manager = TasksManager(storage)


@app.get("/tasks")
def get_tasks():
    return manager.get_tasks()


@app.post("/tasks")
def create_task(task_name: str):
    return manager.create_task(task_name)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_name: str = None, status: str = None):
    return manager.update_task(task_id, task_name, status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return manager.delete_task(task_id)
