from pathlib import Path

import boto3
import pytest
from moto import (
    mock_dynamodb,
    mock_events,
    mock_s3,
    mock_scheduler,
    mock_sqs,
    mock_stepfunctions,
)
from mypy_boto3_s3 import S3Client

from data_ingestion import settings
from data_ingestion.database.SetupDB import create_data_ingestion_metadata_table
from data_ingestion.settings import DATA_INGESTION_BUCKET
from data_ingestion.utils.common import (
    DATA_INGESTION_EVENT_BUS,
    DATA_INGESTION_METADATA_TABLE,
)

AWS_REGION = settings.AWS_REGION


@pytest.fixture()
def dynamodb_client():
    with mock_dynamodb():
        yield boto3.client("dynamodb", region_name=AWS_REGION)


@pytest.fixture()
def mock_create_data_ingestion_metadata_table(dynamodb_client):
    create_data_ingestion_metadata_table(dynamodb_client)


@pytest.fixture()
def s3_client():
    with mock_s3():
        yield boto3.client("s3", region_name=AWS_REGION)


@pytest.fixture()
def scheduler_client():
    with mock_scheduler():
        yield boto3.client("scheduler", region_name=AWS_REGION)


@pytest.fixture()
def step_functions_client():
    with mock_stepfunctions():
        yield boto3.client("stepfunctions", region_name=AWS_REGION)


@pytest.fixture()
def eventbridge_client():
    with mock_events():
        yield boto3.client("events", region_name=AWS_REGION)


@pytest.fixture()
def sqs_client():
    with mock_sqs():
        yield boto3.client("sqs", region_name=AWS_REGION)


@pytest.fixture()
def mocked_scheduler_client(mocker):
    mocker.patch(
        "data_ingestion.aws_services.scheduler_service.scheduler_client.create_schedule",
        return_value=None,
    )


@pytest.fixture()
def mocked_export_table(mocker):
    mocker.patch(
        "data_ingestion.handler.initiate_export_handler.dynamodb_client.export_table_to_point_in_time",
        return_value={"ExportDescription": {"ExportArn": "test arn"}},
    )


@pytest.fixture()
def mock_create_bucket(s3_client: S3Client):
    s3_client.create_bucket(
        Bucket=DATA_INGESTION_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
    )


@pytest.fixture()
def mock_describe_export(mocker):
    mocker.patch(
        "data_ingestion.handler.s3_folder_refiner.dynamodb_client.describe_export",
        return_value={"ExportDescription": {"ExportType": "FULL_EXPORT"}},
    )


@pytest.fixture()
def mock_upload_file_full_export(s3_client: S3Client, mock_create_bucket):
    EXPORT_FOLDER = "export/AWSDynamoDB/01793685827463-3e8752fd"
    curr_dir = Path(__file__).parent.as_posix()
    s3_client.upload_file(
        Bucket=DATA_INGESTION_BUCKET,
        Key=f"{EXPORT_FOLDER}/manifest-files.json",
        Filename=f"{curr_dir}/handler/test_data/manifest-files.json",
    )
    s3_client.upload_file(
        Bucket=DATA_INGESTION_BUCKET,
        Key=f"{EXPORT_FOLDER}/data/data-file.json",
        Filename=f"{curr_dir}/handler/test_data/data-file.json.gz",
    )


@pytest.fixture()
def mock_add_export_status_record(
    dynamodb_client, mock_create_data_ingestion_metadata_table
):
    dynamodb_client.put_item(
        TableName=DATA_INGESTION_METADATA_TABLE,
        Item={
            "PK": {"S": "TABLE#TableName"},
            "SK": {"S": "RANGE#1711619556210-1711619556219"},
            "export_arn": {"S": ""},
            "export_from_time": {"N": "1711619556210"},
            "export_to_time": {"N": "1711619556219"},
            "export_type": {"S": "INCREMENTAL_EXPORT"},
            "export_status": {"S": "IN_PROGRESS"},
            "export_sequence": {"S": "export_1"},
        },
    )


@pytest.fixture()
def mock_add_config_record(dynamodb_client, mock_create_data_ingestion_metadata_table):
    dynamodb_client.put_item(
        TableName=DATA_INGESTION_METADATA_TABLE,
        Item={
            "PK": {"S": "TABLE_CONFIG#table"},
            "SK": {"S": "CONFIGTIME#122792905"},
            "domain_file": {"S": "test"},
            "cron": {"S": "0 0 * * ? *"},
            "status": {"S": "enabled"},
            "is_active": {"S": "true"},
        },
    )
    dynamodb_client.put_item(
        TableName=DATA_INGESTION_METADATA_TABLE,
        Item={
            "PK": {"S": "TABLE_CONFIG#table"},
            "SK": {"S": "CONFIGTIME#latest"},
            "latest_timestamp": {"N": "122792905"},
        },
    )


@pytest.fixture()
def mock_create_event_bus(eventbridge_client):
    eventbridge_client.create_event_bus(Name=DATA_INGESTION_EVENT_BUS)
