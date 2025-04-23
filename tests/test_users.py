import pytest

from litestar.status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from litestar.testing import TestClient
from src.db.models import User
from src.db.repositories import UserRepository


@pytest.mark.asyncio
async def test_create_user(test_client: TestClient, user_repository: UserRepository):
    """Test creating a new user."""
    # Prepare data
    user_data = {"name": "John", "surname": "Doe", "password": "password123"}

    # Send request
    response = await test_client.post("/users", json=user_data)

    # Check response
    assert response.status_code == HTTP_201_CREATED
    user = response.json()
    assert user["name"] == user_data["name"]
    assert user["surname"] == user_data["surname"]
    assert "id" in user
    assert "created_at" in user
    assert "updated_at" in user
    assert "password" not in user

    # Check database
    db_user = await user_repository.get(user["id"])
    assert db_user is not None
    assert db_user.name == user_data["name"]
    assert db_user.surname == user_data["surname"]
    assert db_user.password == user_data["password"]


@pytest.mark.asyncio
async def test_get_users(test_client: TestClient, user_repository: UserRepository):
    """Test getting list of users."""
    # Create test users
    users = [
        User(name="John", surname="Doe", password="password1"),
        User(name="Jane", surname="Smith", password="password2"),
    ]

    for user in users:
        await user_repository.add(user)
    await user_repository.commit()

    # Send request
    response = await test_client.get("/users")

    # Check response
    assert response.status_code == HTTP_200_OK
    users_list = response.json()
    assert len(users_list) == 2
    assert all("password" not in user for user in users_list)
    assert {user["name"] for user in users_list} == {"John", "Jane"}


@pytest.mark.asyncio
async def test_get_user(test_client: TestClient, user_repository: UserRepository):
    """Test getting a single user."""
    # Create test user
    user = User(name="John", surname="Doe", password="password123")
    await user_repository.add(user)
    await user_repository.commit()

    # Send request
    response = await test_client.get(f"/users/{user.id}")

    # Check response
    assert response.status_code == HTTP_200_OK
    user_data = response.json()
    assert user_data["id"] == user.id
    assert user_data["name"] == user.name
    assert user_data["surname"] == user.surname
    assert "password" not in user_data


@pytest.mark.asyncio
async def test_update_user(test_client: TestClient, user_repository: UserRepository):
    """Test updating a user."""
    # Create test user
    user = User(name="John", surname="Doe", password="password123")
    await user_repository.add(user)
    await user_repository.commit()

    # Prepare update data
    update_data = {"name": "John Updated", "surname": "Doe Updated"}

    # Send request
    response = await test_client.put(f"/users/{user.id}", json=update_data)

    # Check response
    assert response.status_code == HTTP_200_OK
    user_data = response.json()
    assert user_data["name"] == update_data["name"]
    assert user_data["surname"] == update_data["surname"]

    # Check database
    updated_user = await user_repository.get(user.id)
    assert updated_user.name == update_data["name"]
    assert updated_user.surname == update_data["surname"]
    assert updated_user.password == user.password  # Password should remain unchanged


@pytest.mark.asyncio
async def test_delete_user(test_client: TestClient, user_repository: UserRepository):
    """Test deleting a user."""
    # Create test user
    user = User(name="John", surname="Doe", password="password123")
    await user_repository.add(user)
    await user_repository.commit()

    # Send request
    response = await test_client.delete(f"/users/{user.id}")

    # Check response
    assert response.status_code == HTTP_204_NO_CONTENT

    # Check database
    with pytest.raises(Exception):  # Should raise an exception as user no longer exists
        await user_repository.get(user.id)


@pytest.mark.asyncio
async def test_get_nonexistent_user(test_client: TestClient):
    """Test getting a nonexistent user."""
    # Send request with non-existent ID
    response = await test_client.get("/users/999999")

    # Check response
    assert response.status_code == 404
