import json

from data_ingestion.utils.common import DATA_INGESTION_EVENT_BUS
from data_ingestion.utils.eventbridge_client import create_eventbridge_client
from data_ingestion.utils.logger import configure_logging

logger = configure_logging()
eventbridge_client = create_eventbridge_client()


def put_event(event: dict):
    try:
        response = eventbridge_client.put_events(
            Entries=[
                {
                    "Source": "com.tyme.data-ingestion",
                    "DetailType": "DataIngestion",
                    "Detail": json.dumps(event),
                    "EventBusName": DATA_INGESTION_EVENT_BUS,
                }
            ]
        )
        return response
    except Exception as ex:
        logger.exception(ex)
        raise ex
