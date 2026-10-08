from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db,get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from ..models import Todos
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'codingwithrobytest','id':1,'user_role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)
@pytest.fixture
def test_todos():
    todos = Todos(
        title="Learn to Code",
        description="Need to Learn Everyday!",
        priority=5,
        complete=False,
        owner_id=1
    )
    db=TestingSessionLocal()
    db.add(todos)
    db.commit()
    yield todos
    with engine.connect() as connection:
        connection.execute(text("Delete from todos;"))
        connection.commit()

def test_read_all_authenticated(test_todos):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False,'title':'Learn to Code',
                                'description':'Need to Learn Everyday!',
                                'id':1,'priority':5,'owner_id':1}]


def test_read_one_authenticated(test_todos):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete':False,'title':'Learn to Code',
                                'description':'Need to Learn Everyday!',
                                'id':1,'priority':5,'owner_id':1}

def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todos):
    request_data={
        'title':'New Todo!',
        'description':'New Todo Description!',
        'priority':5,
        'complete':False,
    }
    response = client.post("/todos", json=request_data)
    assert response.status_code == 201
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')



def test_update_todo(test_todos):
    request_data={
        'title':'Change the title of the todo already saved!',
        'description':'Need to Learn Everyday!',
        'priority':5,
        'complete':False,
    }
    response=client.put("/todos/1",json=request_data)
    assert response.status_code == 200
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model.title == 'Change the title of the todo already saved!'


def test_update_todo_not_found(test_todos):
    request_data={
        'title':'Change the title of the todo already saved!',
        'description':'Need to Learn Everyday!',
        'priority':5,
        'complete':False,
    }
    response=client.put("/todos/999",json=request_data)
    assert response.status_code == 404
    assert response.json()=={'detail':'Todo not found'}

def test_delete_todo(test_todos):
    response=client.delete("/todos/1")
    assert response.status_code == 204
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None

def test_delete_todo_not_found(test_todos):
    response=client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()=={'detail':'Todo not found'}



