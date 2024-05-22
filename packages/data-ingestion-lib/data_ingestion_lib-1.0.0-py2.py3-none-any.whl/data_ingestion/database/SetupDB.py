from mypy_boto3_dynamodb import DynamoDBClient

from data_ingestion.utils import common

DATA_INGESTION_METADATA_TABLE = common.DATA_INGESTION_METADATA_TABLE


def create_data_ingestion_metadata_table(dynamodb_client: DynamoDBClient):
    existing_tables = dynamodb_client.list_tables()["TableNames"]
    if DATA_INGESTION_METADATA_TABLE not in existing_tables:
        response = dynamodb_client.create_table(
            TableName=DATA_INGESTION_METADATA_TABLE,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "is_active", "AttributeType": "S"},
                {"AttributeName": "domain_file", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "IsActiveIndex",
                    "KeySchema": [
                        {"AttributeName": "domain_file", "KeyType": "HASH"},
                        {"AttributeName": "is_active", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "INCLUDE",
                        "NonKeyAttributes": ["PK", "SK"],
                    },
                }
            ],
        )
        return response
