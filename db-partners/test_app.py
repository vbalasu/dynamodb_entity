import requests, app, os
mode = os.environ.get('APP_MODE')
if mode == 'STAGING':
    url = 'https://msqmykjwde.execute-api.us-east-1.amazonaws.com/api'
elif mode == 'PROD':
    url = 'https://db-partners.databricks-partners.com'
else:
    url = 'http://127.0.0.1:8000'

def test_dict_to_dynamo_dict():
    assert app.dict_to_dynamo_dict({'hello': 'world'}) == {'hello': {'S': 'world'}}

def test_home():
    response = requests.get(url)
    assert response.status_code == 200

def test_put():
    # echo '{"data": "two", "id": "second"}' | http PUT http://127.0.0.1:8000/put/db_partners_items
    response = requests.put(f'{url}/put/db_partners_items', json={'id': 'second', 'data': 'two'})
    assert response.status_code == 200

def test_get():
    response = requests.get(f'{url}/get/second/db_partners_items')
    assert response.status_code == 200

def test_list():
    response = requests.get(f'{url}/list/db_partners_items')
    assert response.status_code == 200

def test_delete():
    response = requests.get(f'{url}/delete/second/db_partners_items')
    assert response.status_code == 200