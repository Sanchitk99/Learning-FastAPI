from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todos):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False,'title':'Learn to Code',
                                'description':'Need to Learn Everyday!','id':1,
                                'priority':5,'owner_id':1}]

def test_admin_delete_todo_authenticated(test_todos):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204
    # Verify that the todo is deleted from the database
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todos):
    response = client.delete("/admin/todo/999")  # Assuming 999 is a non-existent ID
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}