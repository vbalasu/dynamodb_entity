from chalice import Chalice

app = Chalice(app_name='dynamodb-links')

import socket, os
host = socket.gethostname()
if os.environ.get('MODE') == 'PRODUCTION':
    profile_name = 'vbalasu_admin'  # 'aws-field-eng_databricks-power-user'
    endpoint_url = None
else:   # Local development
    profile_name = 'fake'
    endpoint_url = 'http://localhost:8000'

def get(id, TableName='items'):
    import boto3
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.get_item(TableName=TableName, Key={'id': {'S': id }})
    return result['Item']

def delete(id, TableName='items'):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    try:
        result = dynamodb.delete_item(TableName=TableName, Key={'id':{'S': id}})
    except ClientError:
        return True
    if result:
        return True

def put(object, TableName='items'):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.put_item(TableName=TableName, Item=object)
    if result:
        return True

def list(TableName='items'):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.scan(TableName=TableName)
    return result['Items'] 

def query(partiql_statement):
    import boto3
    from botocore.errorfactory import ClientError
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
    result = dynamodb.execute_statement(Statement=partiql_statement)
    return result['Items'] 

class Entity:
    def __init__(self, TableName='items'):
        self.TableName = TableName
    def create_table(self):
        import boto3
        from botocore.errorfactory import ClientError
        session = boto3.Session(profile_name=profile_name)
        dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
        dynamodb.create_table(AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            ],
            TableName=self.TableName,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            BillingMode='PAY_PER_REQUEST')
        return True
    def delete_table(self):
        import boto3
        from botocore.errorfactory import ClientError
        session = boto3.Session(profile_name=profile_name)
        dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
        dynamodb.delete_table(TableName=self.TableName)
        return True
    def put(self, object):
        return put(object, TableName=self.TableName)
    def get(self, id):
        return get(id, self.TableName)
    def query(self, partiql_statement):
        return query(partiql_statement)
    def list(self):
        return list(self.TableName)
    def delete(self, id):
        return delete(id, self.TableName)
    

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
