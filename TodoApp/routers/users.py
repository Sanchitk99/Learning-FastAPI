from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..database import SessionLocal
from passlib.context import CryptContext

from ..models import Todos, Users
from .auth import get_current_user

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)
def get_db():  # Define a function to get a database session.
    db = SessionLocal()  # Create a new database session.
    try:
        yield db  # Yield the database session to the caller.
    finally:
        db.close()  # Close the database session when done.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str =Field(min_length=8 )

@router.get("/",status_code=status.HTTP_200_OK)
async def get_users(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,db:db_dependency,user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    user_model=db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401,detail="Error in Password Change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phonenumber/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency,db:db_dependency,phone_number:str):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    user_model=db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
