from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from database import SessionLocal
from models import Todos
from .auth import get_current_user

router = APIRouter()

def get_db():  # Define a function to get a database session.
    db = SessionLocal()  # Create a new database session.
    try:
        yield db  # Yield the database session to the caller.
    finally:
        db.close()  # Close the database session when done.


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id==user.get("id")).all()

@router.get("/todos/{todo_id}")
async def read_todo(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail=f"Todo with id {todo_id} not found")
    return todo_model


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,db: db_dependency,todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(),owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}")
async def update_todo(user:user_dependency,db: db_dependency
                      ,todo_request: TodoRequest
                      ,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}")
async def delete_todo(user:user_dependency,db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).delete()
    db.commit()

