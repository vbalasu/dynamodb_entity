from chalicelib import dynamodb_entity as entity

def test_put():
    result = entity.put({'data': {'S': 'world'}, 'id': {'S': 'hello'}}, TableName='db_partners_items')
    assert result is True
    print('test_put complete')
    
def test_get():
    result = entity.get('hello', TableName='db_partners_items')
    assert result == {'data': {'S': 'world'}, 'id': {'S': 'hello'}}
    print('test_get complete')

def test_query():
    result = entity.query("SELECT * FROM db_partners_items WHERE id='hello'")
    assert type(result) == list
    print('test_query complete')

def test_list():
    result = entity.list(TableName='db_partners_items')
    assert type(result) == list
    print('test_list complete')

def test_delete():
    result = entity.delete('hello', TableName='db_partners_items')
    assert result is True
    print('test_delete complete')

def test_Entity():
    temp_to_delete = entity.Entity('db_partners_temp')
    assert type(temp_to_delete) == entity.Entity
    print('test_Entity complete')

def test_Entity_create_table():
    temp_to_delete = entity.Entity('db_partners_temp')
    assert temp_to_delete.create_table() is True
    print('test_Entity_create_table complete')

def test_Entity_dml_operations():
    temp_to_delete = entity.Entity('db_partners_temp')
    temp_to_delete.put({'data': {'S': 'world'}, 'id': {'S': 'hello'}})
    temp_to_delete.get('hello')
    temp_to_delete.query("SELECT * FROM db_partners_temp WHERE id='hello'")
    temp_to_delete.list()
    temp_to_delete.delete('hello')
    print('test_Entity_dml_operations complete')

def test_Entity_delete_table():
    temp_to_delete = entity.Entity('db_partners_temp')
    assert temp_to_delete.delete_table() is True
    print('test_Entity_delete_table complete')

