from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()

# Base == declarative_base

models.Base.metadata.create_all(bind=engine)

# uvicorn main:app --reload


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# BaseModel only for JavaScript != declarative_base, for DB

class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }

@app.post("/")
async def create_todo ( todo: Todo, db: Session = Depends(get_db) ) :

    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = 0

    db.add(todo_model)
    db.commit()

    return successful_response(201)

