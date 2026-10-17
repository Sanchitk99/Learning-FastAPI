from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_current_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithrobytest'
    assert response.json()['email'] == 'codingwithrobytest@email.com'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'


def test_change_password_success(test_user):
    response=client.put("/users/password",json={"password":"testpassword",
                                            "new_password":"newpassword"})
    assert response.status_code==status.HTTP_204_NO_CONTENT



def test_change_password_invalid_current_password(test_user):
    response=client.put("/users/password",json={"password":"wrongpassword",
                                            "new_password":"newpassword"})
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Error on Password Change'}

def test_change_phone_number(test_user):
    response=client.put("/users/phonenumber/(222)-222-2222")
    assert response.status_code==status.HTTP_204_NO_CONTENT     