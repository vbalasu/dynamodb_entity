import os, toml

mode = os.environ.get('APP_MODE')
try:
    # First look for app.toml in the application root
    with open('app.toml') as f:
        config = toml.load(f)
except:
    # Then look in the same directory as the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{script_dir}/app.toml') as f:
        config = toml.load(f)

try:
    endpoint_url = config[mode]['endpoint_url']
except:
    endpoint_url = None
try:
    profile_name = config[mode]['profile_name']
except:
    profile_name = None

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
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=self.TableName)
        return True
    def delete_table(self):
        import boto3
        from botocore.errorfactory import ClientError
        session = boto3.Session(profile_name=profile_name)
        dynamodb = session.client('dynamodb', endpoint_url=endpoint_url)
        dynamodb.delete_table(TableName=self.TableName)
        waiter = dynamodb.get_waiter('table_not_exists')
        waiter.wait(TableName=self.TableName)
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
    
