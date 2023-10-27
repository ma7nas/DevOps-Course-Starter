import pytest
import requests
import os
from dotenv import load_dotenv, find_dotenv
from todo_app import app


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

created_items = []
def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    global created_items

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '1a2b3c',
            'name': 'To Do',
            'cards': [{'id': '123', 'name': 'Test card 1'},{'id': '456', 'name': 'Test card 2'}]
        }]
        fake_response_data[0]['cards'].extend(created_items)
        return StubResponse(fake_response_data)
    elif url.startswith('https://api.trello.com/1/cards'):
        fake_response_data = [{
            'id': '1223def'
        }]
        created_items.append({'id': '1223def', 'name': 'Test add item'})
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', stub)

    # Make a request to our app's index page
    response = client.get('/')

    # Check the response code and the data in the response
    assert response.status_code == 200
    assert '123' in response.data.decode()
    assert 'Test card 2' in response.data.decode()

def test_add_end_point(monkeypatch, client):
    # Replace requests.post(url) with our own function
    monkeypatch.setattr(requests, 'post', stub)

    # Make a request to add a to do item
    to_do_list_id = os.environ.get('TRELLO_TODO_LIST_ID')
    payload = {'name': 'Test add item', 'idList': to_do_list_id}
    
    post_response = client.post('/add', data=payload)

    # Replace requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', stub)

    # Perform the redirect here ourselves using monkeypatch data
    get_response = client.get('/')

    # Check the post response performs a redirect (302), the get response code (200) and the newly added data
    assert post_response.status_code == 302
    assert get_response.status_code == 200
    assert 'Test add item' in get_response.data.decode()