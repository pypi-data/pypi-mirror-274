"""CRUD for data_ingestion_metadata_table."""

from http import HTTPStatus

from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient

from data_ingestion.model.data_ingestion_metadata_table.DataIngestionConfig import (
    DataIngestionConfig,
    config_from_dynamodb_item,
)
from data_ingestion.utils.common import DATA_INGESTION_METADATA_TABLE
from data_ingestion.utils.logger import configure_logging

logger = configure_logging()


def get_latest_config(table: str, dynamodb_client: DynamoDBClient):
    try:
        response = dynamodb_client.query(
            TableName=DATA_INGESTION_METADATA_TABLE,
            KeyConditionExpression="PK = :PK",
            ExpressionAttributeValues={
                ":PK": {"S": f"TABLE_CONFIG#{table}"},
            },
            FilterExpression="attribute_not_exists(latest_timestamp)",
            ScanIndexForward=False,
            Limit=2,
        )
        item = response.get("Items")
        if item:
            return config_from_dynamodb_item(item[0])
        return None
    except Exception as ex:
        logger.exception(ex)
        raise ex


def remove_is_active(item: DataIngestionConfig, dynamodb_client: DynamoDBClient):
    try:
        response = dynamodb_client.update_item(
            TableName=DATA_INGESTION_METADATA_TABLE,
            Key=item.primary_key(),
            UpdateExpression="REMOVE is_active",
            ConditionExpression="attribute_exists(is_active)",
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]
    except Exception as ex:
        logger.exception(ex)
        raise ex


def get_active_config(domain: str, dynamodb_client: DynamoDBClient):
    try:
        response = dynamodb_client.query(
            TableName=DATA_INGESTION_METADATA_TABLE,
            IndexName="IsActiveIndex",
            KeyConditionExpression="domain_file = :domain AND is_active = :active",
            ExpressionAttributeValues={
                ":domain": {"S": domain},
                ":active": {"S": "true"},
            },
        )
        items = response.get("Items")
        if items:
            return [config_from_dynamodb_item(item) for item in items]
        return []
    except Exception as ex:
        logger.exception(ex)
        raise ex


def add_config(item: dict, dynamodb_client: DynamoDBClient):
    """
    Add data ingestion configuration item to DynamoDB
    """
    try:
        response = dynamodb_client.put_item(
            TableName=DATA_INGESTION_METADATA_TABLE,
            Item=item,
            ConditionExpression="attribute_not_exists(SK)",
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.info("add_config: the item already exists")
            return HTTPStatus.CONFLICT
        else:
            logger.exception(err)
            raise err
    except Exception as ex:
        logger.exception(ex)
        raise ex


def add_latest_item(table: str, timestamp: str, dynamodb_client: DynamoDBClient):
    try:
        res = dynamodb_client.put_item(
            TableName=DATA_INGESTION_METADATA_TABLE,
            Item={
                "PK": {
                    "S": f"TABLE_CONFIG#{table}",
                },
                "SK": {"S": "CONFIGTIME#latest"},
                "latest_timestamp": {"N": timestamp},
            },
            ConditionExpression="attribute_not_exists(latest_timestamp) OR latest_timestamp < :lt",
            ExpressionAttributeValues={":lt": {"N": timestamp}},
        )
        return res["ResponseMetadata"]["HTTPStatusCode"]
    except ClientError as ex:
        if ex.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.info(
                "add_latest_item: timestamp is older than the current timestamp"
            )
            return HTTPStatus.CONFLICT
        else:
            logger.exception(ex)
            raise ex
