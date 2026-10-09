from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth,todos,admin,users

app=FastAPI()

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
Base.metadata.create_all(bind=engine) # Create the database tables based on the defined models. This line ensures that the tables are created in the database if they do not already exist.

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
