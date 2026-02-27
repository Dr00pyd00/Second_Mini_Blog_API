from fastapi.testclient import TestClient


# ================================================================
# ===================== CREATE POSTS =============================
# ================================================================

# ----------- SUCCESS ------------ #

# create new post success


def test_create_post_success(client: TestClient, create_user, auth_header):

    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }
    response = client.post(
        "posts",
        headers=auth_header,
        json=post_data,
          )

    assert response.status_code == 201


# ------------- FAILURE -------------- #

# no authenticate user ( no token)
def test_create_post_not_authenticate(client: TestClient):
    
    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }
    response = client.post(
        "posts",
        json=post_data,
          )
    assert response.status_code == 401
    assert "not authenticate" in response.text.lower()

# token not valid
def test_create_post_invalid_jwt(client: TestClient):
    
    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }
    response = client.post(
        "posts",
        json=post_data,
        headers={"Authorization":"Bearer bad_token"}
          )
    assert response.status_code == 401
    assert "invalid jwt credentials" in response.text.lower()



 
# ================================================================
# ===================== UPDATE POSTS =============================
# ================================================================



# ----------- SUCCESS ------------ #

# a user update a post
def test_update_post_success(client: TestClient, create_user, auth_header, create_post):

    # create post and get id : create_user + create_post 
    
    # be sure the user is owner
    assert create_post.json()["owner"]["id"] == create_user.json()["id"]

    # update :

    data_to_update = {
        "title": "UPDATED",
    }

    response = client.patch(f"posts/{create_post.json()["id"]}",
                            headers=auth_header,
                            json=data_to_update)
    
    assert response.status_code == 200
    assert response.json()["title"] == "UPDATED"


# ------------- FAILURE -------------- #


# user update a post that not own 
def test_update_post_not_owner(client: TestClient, create_user, auth_header, create_post):

    other_user = client.post("users", json={
        "username": "otheruser",
        "password": "test123"
    })
    other_token = client.post("login", data={
        "username": "otheruser",
        "password": "test123"
    }).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # be sure the user are different
    assert create_user.json()["id"] != other_user.json()["id"]

    # update with other_user:

    data_to_update = {
        "title": "UPDATED",
    }

    response = client.patch(f"posts/{create_post.json()["id"]}",
                            headers=other_headers,
                            json=data_to_update)

    assert response.status_code == 403
    assert "not owner" in response.text.lower()

# update post with inexistant field 

def test_update_post_inexistant_field(client: TestClient, create_user, auth_header, create_post):

    # create post and get id : create_user + create_post 
    
    # be sure the user is owner
    assert create_post.json()["owner"]["id"] == create_user.json()["id"]

    # update :

    data_to_update = {
        "inexistant_field": "UPDATED",
    }

    response = client.patch(f"posts/{create_post.json()["id"]}",
                            headers=auth_header,
                            json=data_to_update)
    
    assert response.status_code == 422
    assert "extra_forbidden" in response.text