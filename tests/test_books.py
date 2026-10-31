def test_create_book_as_user(client, user_headers, sample_book):
    response = client.post("/books", json=sample_book, headers=user_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Clean Code"


def test_get_all_books(client, user_headers, sample_book):
    client.post("/books", json=sample_book, headers=user_headers)
    response = client.get("/books", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_book_by_id(client, user_headers, sample_book):
    book_id = client.post("/books", json=sample_book, headers=user_headers).json()["id"]
    response = client.get(f"/books/{book_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["id"] == book_id


def test_get_nonexistent_book(client, user_headers):
    assert client.get("/books/9999", headers=user_headers).status_code == 404


def test_create_book_negative_price(client, user_headers):
    bad = {"title": "Bad", "author": "Nobody", "price": -5}
    response = client.post("/books", json=bad, headers=user_headers)
    assert response.status_code in (400, 422)


def test_create_book_missing_title(client, user_headers):
    response = client.post(
        "/books", json={"author": "Nobody", "price": 5}, headers=user_headers
    )
    assert response.status_code == 422


def test_books_require_token(client, sample_book):
    assert client.get("/books").status_code == 401
    assert client.post("/books", json=sample_book).status_code == 401


def test_user_cannot_update_book(client, user_headers, sample_book):
    book_id = client.post("/books", json=sample_book, headers=user_headers).json()["id"]
    response = client.put(f"/books/{book_id}", json=sample_book, headers=user_headers)
    assert response.status_code == 403


def test_user_cannot_delete_book(client, user_headers, sample_book):
    book_id = client.post("/books", json=sample_book, headers=user_headers).json()["id"]
    response = client.delete(f"/books/{book_id}", headers=user_headers)
    assert response.status_code == 403


def test_admin_can_update_book(client, user_headers, admin_headers, sample_book):
    book_id = client.post("/books", json=sample_book, headers=user_headers).json()["id"]
    updated = {**sample_book, "title": "Clean Code 2nd Edition"}
    response = client.put(f"/books/{book_id}", json=updated, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Clean Code 2nd Edition"


def test_admin_can_delete_book(client, user_headers, admin_headers, sample_book):
    book_id = client.post("/books", json=sample_book, headers=user_headers).json()["id"]
    response = client.delete(f"/books/{book_id}", headers=admin_headers)
    assert response.status_code == 204
    assert client.get(f"/books/{book_id}", headers=user_headers).status_code == 404


def test_admin_update_nonexistent_book(client, admin_headers, sample_book):
    response = client.put("/books/9999", json=sample_book, headers=admin_headers)
    assert response.status_code == 404


def test_admin_delete_nonexistent_book(client, admin_headers):
    assert client.delete("/books/9999", headers=admin_headers).status_code == 404