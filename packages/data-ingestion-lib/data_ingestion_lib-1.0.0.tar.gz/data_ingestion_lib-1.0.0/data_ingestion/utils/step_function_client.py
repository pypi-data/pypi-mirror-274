from boto3.session import Session

from data_ingestion import settings
from data_ingestion.utils.aws_session import create_custom_session

_ENV = settings.ENV
_LOCAL_STEP_FUNCTIONS_ENDPOINT = settings.LOCAL_DYNAMODB_ENDPOINT


def create_step_functions_client():
    session: Session = create_custom_session()
    if _ENV == "local":
        return session.client("stepfunctions")
    return session.client("stepfunctions", region_name=settings.AWS_REGION)
