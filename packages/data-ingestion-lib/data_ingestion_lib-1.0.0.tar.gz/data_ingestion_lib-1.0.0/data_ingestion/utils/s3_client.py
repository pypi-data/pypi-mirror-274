from boto3.session import Session
from mypy_boto3_s3 import S3Client

from data_ingestion import settings
from data_ingestion.utils.aws_session import create_custom_session

_ENV = settings.ENV


def create_s3_client() -> S3Client:
    session: Session = create_custom_session()
    if _ENV == "local":
        return session.client("s3")
    return session.client("s3", region_name=settings.AWS_REGION)
