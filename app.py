from chalice import Chalice

app = Chalice(app_name='dynamodb-links')

import socket
host = socket.gethostname()
if host == 'XGF6JF2F0Q':   # Local development
    profile_name = 'fake'
    endpoint_url = 'http://localhost:8000'
else:
    profile_name = None  # 'aws-field-eng_databricks-power-user'
    endpoint_url = None

def get(id):
    import boto3
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.execute_statement(Statement="SELECT * FROM items WHERE id=?;", Parameters=[{'S': id}])
    return result['Items']

def delete(id):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    try:
        result = dynamodb.execute_statement(Statement="DELETE FROM items WHERE id=?;", Parameters=[{'S': id}])
    except ClientError:
        return True
    if result:
        return True

def insert(object):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    # "{'id': 'two', {'data': 'second'}}"
    result = dynamodb.execute_statement(Statement=f"INSERT INTO items VALUE {str(object)};")
    if result:
        return True

def list():
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.scan(TableName='items')
    return result['Items'] 

def query(partiql_statement):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.execute_statement(Statement=partiql_statement)
    return result['Items'] 


@app.route('/')
def index():
    return {'hello': 'world'}


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
