import app

def test_insert():
    result = app.insert({'id': 'hello', 'data': 'world'})
    assert result is True
    
def test_get():
    result = app.get('hello')
    assert result == [{'data': {'S': 'world'}, 'id': {'S': 'hello'}}]

def test_query():
    result = app.query("SELECT * FROM items WHERE id='hello'")
    assert type(result) == list

def test_list():
    result = app.list()
    assert type(result) == list

def test_delete():
    result = app.delete('hello')
    assert result is True

