from mypy_boto3_dynamodb import DynamoDBClient

from data_ingestion.model.data_ingestion_metadata_table.ExportStatus import (
    ExportStatus,
    export_status_from_dynamodb_item,
)
from data_ingestion.utils.common import DATA_INGESTION_METADATA_TABLE, DBExportStatus
from data_ingestion.utils.logger import configure_logging

logger = configure_logging()


def get_last_export_by_table_name(table_name: str, dynamodb_client: DynamoDBClient):
    """
    Get last export from DynamoDB by table name
    """
    try:
        response = dynamodb_client.query(
            TableName=DATA_INGESTION_METADATA_TABLE,
            KeyConditionExpression="PK = :PK",
            ExpressionAttributeValues={
                ":PK": {"S": f"TABLE#{table_name}"},
            },
            ScanIndexForward=False,
            Limit=1,
        )
        items = response.get("Items")
        if items:
            return export_status_from_dynamodb_item(items[0])
        return None
    except Exception as ex:
        logger.exception(ex)
        raise ex


def get_export_status_by_keys(pk: str, sk: str, dynamodb_client: DynamoDBClient):
    """
    Get export status from DynamoDB by primary key and sort key
    """
    try:
        response = dynamodb_client.get_item(
            TableName=DATA_INGESTION_METADATA_TABLE,
            Key={
                "PK": {"S": pk},
                "SK": {"S": sk},
            },
        )
        item = response.get("Item")
        if item:
            return export_status_from_dynamodb_item(item)
        return None
    except Exception as ex:
        logger.exception(ex)
        raise ex


def add_export_status(item: dict, dynamodb_client: DynamoDBClient):
    """
    Add export status item to DynamoDB
    """
    try:
        response = dynamodb_client.put_item(
            TableName=DATA_INGESTION_METADATA_TABLE,
            Item=item,
        )
        return response
    except Exception as ex:
        logger.exception(ex)
        raise ex


def upsert_export_item(item: ExportStatus, dynamodb_client: DynamoDBClient):
    logger.info(
        f"Start to insert/update an export item of table {item.table_name} with time range {item.sort_key()['SK']['S']}"
    )

    (
        update_expression,
        expression_attr_values,
    ) = item.build_update_expression_with_non_empty_attrs()

    condition_expression: str = (
        "attribute_not_exists(export_status) OR export_status = :failedstatus"
    )
    expression_attr_values[":failedstatus"] = {"S": DBExportStatus.FAILED.value}

    response = dynamodb_client.update_item(
        TableName=DATA_INGESTION_METADATA_TABLE,
        Key=item.primary_key(),
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attr_values,
        ConditionExpression=condition_expression,
        ReturnValues="ALL_OLD",
    )

    if "Attributes" not in response or response["Attributes"] == {}:
        logger.info(
            f"Inserted an export item of table {item.table_name} with time range {item.sort_key()['SK']['S']}"
        )
        return None

    before_item: ExportStatus = export_status_from_dynamodb_item(response["Attributes"])
    logger.info(
        f"Updated status of the export item of table {item.table_name} with time range {item.sort_key()['SK']['S']} "
        f"from {before_item.export_status} to {item.export_status}"
    )

    return before_item


def update_export_status(item: ExportStatus, dynamodb_client: DynamoDBClient):
    """
    Update export status item to DynamoDB
    """
    try:
        (
            update_expression,
            expression_attr_values,
        ) = item.build_update_expression_with_non_empty_attrs()

        response = dynamodb_client.update_item(
            TableName=DATA_INGESTION_METADATA_TABLE,
            Key=item.primary_key(),
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attr_values,
        )
        return response
    except Exception as ex:
        logger.exception(ex)
        raise ex
