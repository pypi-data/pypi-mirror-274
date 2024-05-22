from boto3.session import Session

from data_ingestion import settings

_ENV = settings.ENV
_AWS_REGION = settings.AWS_REGION


def create_custom_session() -> Session:
    if _ENV == "local":
        return Session(region_name=_AWS_REGION)
    return Session()
