from fastapi.testclient import TestClient

from app.models.mixins.status_mixin import StatusEnum
from app.models.users import RoleEnum


# ================================================================
# ===================== CREATE USER ==============================
# ================================================================

# --------- SUCCESS ---------- #
def test_create_normal_user_success(client: TestClient):

    user_data = {
        "username":"testuser",
        "password":"test123",
        "email":"test@test.com"
    }
        
    response = client.post("users", json=user_data)
    data = response.json()

    assert response.status_code == 201
    assert data["role"] == RoleEnum.USER.value
    assert data["username"] == user_data["username"]
    assert data["deleted_at"] == None
    assert data["status"] == StatusEnum.ACTIVE.value


# --------- FAILURE ---------- #

# username already taken:
def test_create_user_username_already_taken(client: TestClient):
 
    user_data = {
        "username":"testuser",
        "password":"test123"
    }
    # create first one
    client.post("users", json=user_data)
    # second : username error
    response = client.post("users", json=user_data)
    data = response.json()

    assert response.status_code == 409
    assert "already taken" in response.text.lower()

# username too low:
def test_create_user_username_too_low(client: TestClient):

    user_data = {
        "username":"te",
        "password":"test123"
    }
    response = client.post("users", json=user_data)

    assert response.status_code == 422 # pydantic error
    assert "string_too_short" in response.text

# username bad chars:
def test_create_user_username_wrong_char(client: TestClient):

    user_data = {
        "username":"testuser@",
        "password":"test123"
    }
    response = client.post("users", json=user_data)

    assert response.status_code == 422
    assert "value_error" in response.text

# password too low:
def test_create_user_password_too_low(client: TestClient):

    user_data = {
        "username":"testuser",
        "password":"t3"
    }
    response = client.post("users", json=user_data)

    assert response.status_code == 422
    assert "string_too_short" in response.text



# password not alphanumeric
def test_create_user_password_not_alphanumeric(client: TestClient):

    user_data = {
        "username":"testuser",
        "password":"testrrr"
    }
    response = client.post("users", json=user_data)

    assert response.status_code == 422
    assert "value_error" in response.text

# email incorrect 
def test_create_user_email_incorrect(client: TestClient):

    user_data = {
        "username":"testuser",
        "password":"testrrr",
        "email":"test"
    }
    response = client.post("users", json=user_data)

    assert response.status_code == 422
    assert "value_error" in response.text

# ================================================================
# ===================== DELETE USER ==============================
# ================================================================

def test_delete_user(client: TestClient, create_user, auth_header):
    
    response = client.delete(
        f"users/{create_user.json()["id"]}",
        headers=auth_header
        )
    
    assert response.status_code == 200
    assert response.json()["deleted_at"]
