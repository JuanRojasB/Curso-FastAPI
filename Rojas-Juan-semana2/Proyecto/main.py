from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
import asyncio

app = FastAPI(title="API Semana 2")

# ==== ENUMS ====
class Status(str, Enum):
    pending = "pending"
    completed = "completed"

# ==== MODELOS ====
class User(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    active: bool = True

class Task(BaseModel):
    title: str = Field(..., min_length=3)
    status: Status = Status.pending
    assigned_to: Optional[int] = None

# ==== "BD" EN MEMORIA ====
users: List[dict] = []
tasks: List[dict] = []

# ==== FUNCIONES ASYNC ====
async def notify(user_id: int, message: str) -> bool:
    await asyncio.sleep(0.3)
    return True

# ==== ENDPOINTS USERS ====
@app.post("/users")
async def create_user(user: User) -> dict:
    new_user = user.dict()
    new_user["id"] = len(users) + 1
    users.append(new_user)
    await notify(new_user["id"], "Welcome!")
    return new_user

@app.get("/users")
def list_users() -> List[dict]:
    return users

# ==== ENDPOINTS TASKS ====
@app.post("/tasks")
def create_task(task: Task) -> dict:
    new_task = task.dict()
    new_task["id"] = len(tasks) + 1
    new_task["created_at"] = datetime.now()
    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}/status")
async def change_task_status(task_id: int, status: Status) -> dict:
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            await notify(t.get("assigned_to", 0), f"Task status changed to {status}")
            return t
    raise HTTPException(status_code=404, detail="Task not found")
