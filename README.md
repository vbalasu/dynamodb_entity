# local-dynamodb

Use this library for easy access to Dynamodb. You can create a dynamodb `Entity`, then use `create_table` to create it and `delete_table` to delete it. Once created, you can perform DML and DQL operations on it - i.e. put, get, query, list, delete, etc. using the entity object.

You can easily switch between local Dynamodb instance running at http://localhost:8000 and a remote AWS profile [MODE=PRODUCTION]

### Link to Jupyter Notebook

[local-dynamodb.ipynb](local-dynamodb.ipynb)

### Link to python module and tests

[dynamodb_entity.py](dynamodb_entity.py)

[test_dynamodb_entity.py](test_dynamodb_entity.py)
