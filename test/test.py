import os


def test_middleware(client_test):
    response = client_test.get(url="/middleware/")
    assert response.status_code == 200
    assert response.json() == {"message": "Middleware is working"}
    assert response.headers["x-method"] == "It was request GET method."


def test_create_author(
                        client_test,
                        data_test_create_author):
    response = client_test.post(
                                url=f"/author/",
                                json=data_test_create_author)
    response_json = response.json()
    assert response_json["name"] == data_test_create_author["name"]
    assert response_json["pseudo"] == data_test_create_author["pseudo"]
    assert response_json["city"] == data_test_create_author["city"]
    assert response.status_code == 201
    os.environ["ID"] = str(response_json["id"])


def test_update_author(
                        client_test,
                        data_test_create_author,
                        data_test_update_author):
    id = os.environ["ID"]
    response = client_test.put(
                                url=f"/author/{id}/",
                                json=data_test_update_author)
    response_json = response.json()
    assert response_json["name"] == data_test_create_author["name"]
    assert response_json["pseudo"] == data_test_update_author["pseudo"]
    assert response_json["city"] == data_test_create_author["city"]
    assert response.status_code == 200


def test_retrive_author(
                        client_test):
    id = os.environ["ID"]
    response = client_test.get(
                                url=f"/author/{id}/")
    response_json = response.json()
    assert response_json["id"] == int(id) 
    assert response.status_code == 200


def test_list_author(
                        client_test):
    response = client_test.get(
                                url=f"/author/")
    assert response.status_code == 200


def test_delete_author(
                        client_test):
    id = os.environ["ID"]
    response = client_test.delete(
                                url=f"/author/{id}/")
    assert response.status_code == 204
