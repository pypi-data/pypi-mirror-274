import boto3

from data_ingestion import settings

_ENV = settings.ENV


def create_sqs_client():
    if _ENV == "local":
        return boto3.client("sqs", region_name=settings.AWS_REGION)
    return boto3.client("sqs")
