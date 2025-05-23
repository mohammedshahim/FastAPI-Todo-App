
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import override_get_db, override_get_current_user, client, TestingSessionLocal, test_todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'complete': False,
        'id': 1,
        'priority': 5,
        'owner_id':1
    }]

def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'complete': False,
        'id': 1,
        'priority': 5,
        'owner_id':1
    }

def test_read_one_authenticated_not_found(test_todo):
    response = client.get('/todos/todo/1999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

def test_create_todo(test_todo):
    request_data = {
        'title': 'New todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.post('/todos/todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']

def test_update_todo(test_todo):
    request_data = {
        'title': 'Change the title of the doto already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }
    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Change the title of the doto already saved!'
    assert model.description == request_data['description']

def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title of the doto already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }
    response = client.put('/todos/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/todo/199')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}