import app

def test_put():
    result = app.put({'data': {'S': 'world'}, 'id': {'S': 'hello'}})
    assert result is True
    
def test_get():
    result = app.get('hello')
    assert result == {'data': {'S': 'world'}, 'id': {'S': 'hello'}}

def test_query():
    result = app.query("SELECT * FROM items WHERE id='hello'")
    assert type(result) == list

def test_list():
    result = app.list()
    assert type(result) == list

def test_delete():
    result = app.delete('hello')
    assert result is True

def test_Entity():
    temp_to_delete = app.Entity('temp_to_delete')
    assert type(temp_to_delete) == app.Entity

def test_Entity_create_table():
    temp_to_delete = app.Entity('temp_to_delete')
    assert temp_to_delete.create_table() is True

def test_Entity_dml_operations():
    temp_to_delete = app.Entity('temp_to_delete')
    temp_to_delete.put({'data': {'S': 'world'}, 'id': {'S': 'hello'}})
    temp_to_delete.get('hello')
    temp_to_delete.query("SELECT * FROM temp_to_delete WHERE id='hello'")
    temp_to_delete.list()
    temp_to_delete.delete('hello')

def test_Entity_delete_table():
    temp_to_delete = app.Entity('temp_to_delete')
    assert temp_to_delete.delete_table() is True

