from typing import Optional, Annotated

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова")
    yield
    print("выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)



class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None




class STask(STaskAdd):
    id: int

tasks = []


@app.post("/tasks")
async def add_task(
        task: Annotated[STaskAdd, Depends()],

):
    tasks.append(task)
    return {"ok": True}


#@app.get("/tasks")
#def get_tasks():
#    task = Task(name="Запиши это видео")
#   return {"data": task}


