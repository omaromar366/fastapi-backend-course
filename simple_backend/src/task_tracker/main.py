from fastapi import FastAPI

app = FastAPI()


class Task:
    def __init__(self, task_id: int, task_name: str, status: str = 'In Work'):
        self.task_name = task_name
        self.task_id = task_id
        self.status = status

    def to_dict(self):
        return {'id': self.task_id, 'name': self.task_name, 'status': self.status}


class TasksFu:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def get_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def create_task(self, task_name: str):
        task = Task(self.next_id, task_name, status='In Work')
        self.tasks.append(task)
        self.next_id += 1
        return task.to_dict()

    def update_task(self, task_id: int, task_name: str = None, status: str = None):
        for task in self.tasks:
            if task.task_id == task_id:
                if task_name:
                    task.task_name = task_name
                if status:
                    task.status = status
                return task.to_dict()
        raise Exception("Task not found")

    def delete_task(self, task_id: int):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return 'Task deleted'
        raise Exception("Task not found")


task_fu = TasksFu()


@app.get("/tasks")
def get_tasks():
    return task_fu.get_tasks()


@app.post("/tasks")
def create_task(task_name: str):
    return task_fu.create_task(task_name)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_name: str = None, status: str = None):
    return task_fu.update_task(task_id, task_name, status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return task_fu.delete_task(task_id)
