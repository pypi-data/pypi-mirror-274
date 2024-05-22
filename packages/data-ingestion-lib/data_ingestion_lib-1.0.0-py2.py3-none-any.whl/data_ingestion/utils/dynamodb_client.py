from boto3.session import Session
from mypy_boto3_dynamodb import DynamoDBClient

from data_ingestion import settings
from data_ingestion.utils.aws_session import create_custom_session

_ENV = settings.ENV


def create_dynamodb_client() -> DynamoDBClient:
    session: Session = create_custom_session()
    if _ENV == "local":
        return session.client("dynamodb")
    return session.client("dynamodb", region_name=settings.AWS_REGION)
