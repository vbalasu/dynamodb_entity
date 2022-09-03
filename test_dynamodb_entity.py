import dynamodb_entity as entity

def test_put():
    result = entity.put({'data': {'S': 'world'}, 'id': {'S': 'hello'}})
    assert result is True
    
def test_get():
    result = entity.get('hello')
    assert result == {'data': {'S': 'world'}, 'id': {'S': 'hello'}}

def test_query():
    result = entity.query("SELECT * FROM items WHERE id='hello'")
    assert type(result) == list

def test_list():
    result = entity.list()
    assert type(result) == list

def test_delete():
    result = entity.delete('hello')
    assert result is True

def test_Entity():
    temp_to_delete = entity.Entity('temp_to_delete')
    assert type(temp_to_delete) == entity.Entity

def test_Entity_create_table():
    temp_to_delete = entity.Entity('temp_to_delete')
    assert temp_to_delete.create_table() is True

def test_Entity_dml_operations():
    temp_to_delete = entity.Entity('temp_to_delete')
    temp_to_delete.put({'data': {'S': 'world'}, 'id': {'S': 'hello'}})
    temp_to_delete.get('hello')
    temp_to_delete.query("SELECT * FROM temp_to_delete WHERE id='hello'")
    temp_to_delete.list()
    temp_to_delete.delete('hello')

def test_Entity_delete_table():
    temp_to_delete = entity.Entity('temp_to_delete')
    assert temp_to_delete.delete_table() is True

def test_config():
    import os
    mode = os.environ.get('APP_MODE')
    # Remember to set environment variable APP_MODE=DEV on the command line
    print('endpoint_url:', entity.endpoint_url, ' profile_name:', entity.profile_name)
    if mode == 'DEV':
        assert entity.endpoint_url == 'http://localhost:8000'
        assert entity.profile_name == 'fake'
    elif mode == 'PROD':
        assert entity.profile_name is None
    