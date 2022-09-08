from chalice import Chalice
from chalicelib import dynamodb_entity as entity

app = Chalice(app_name='db-partners')


@app.route('/test')
def test():
    from chalicelib import test_databricks
    test_databricks.test_Entity_create_table()
    test_databricks.test_Entity_dml_operations()
    test_databricks.test_Entity_delete_table()
    print('Tests complete')
    return 'Tests complete!'

@app.route('/')
def index():
    return {'hello': 'world'}

# http http://127.0.0.1:8000/get/hello/items
@app.route('/get/{id}/{TableName}')
def get(id, TableName):
    return entity.get(id, TableName)

# http http://127.0.0.1:8000/delete/second/items
@app.route('/delete/{id}/{TableName}')
def delete(id, TableName):
    return entity.delete(id, TableName)

def dict_to_dynamo_dict(mydict):
    from dynamodb_json import json_util as djson
    import json
    data = json.loads(djson.dumps(mydict))
    return data


# echo '{"data": {"S": "two"}, "id": {"S": "second"}}' | http PUT http://127.0.0.1:8000/put/items
@app.route('/put/{TableName}', methods=['PUT'])
def put(TableName):
    data = dict_to_dynamo_dict(app.current_request.json_body)
    return entity.put(data, TableName)

# http http://127.0.0.1:8000/list/items
@app.route('/list/{TableName}')
def list(TableName):
    return entity.list(TableName)

# echo "SELECT * FROM items WHERE id='hello'"|http post http://127.0.0.1:8000/query
@app.route('/query', methods=['POST'])
def query():
    return entity.query(app.current_request.raw_body.decode())




# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
