from data_ingestion.aws_services import s3_service

import yaml
import pytest
from settings import DATA_INGESTION_BUCKET

def test_get_s3_config(
    s3_client,
    mock_create_bucket,
):
    yaml_content = {
        "testing": {
            "test_table": {
                "CronExpression": "0 0 * * ? *"
            }   
        }
    } 
    with open("test.yaml","w") as f: 
        yaml.dump(yaml_content, f, default_flow_style=False)
        s3_client.upload_file(
            Filename="test.yaml",
            Bucket=DATA_INGESTION_BUCKET,
            Key="test.yaml"
        )

        result = s3_service.get_s3_config(
            bucket=DATA_INGESTION_BUCKET,
            key="test.yaml",
            domain="testing",
            s3_client=s3_client
        )

        assert result["test_table"] == "0 0 * * ? *"
        
        empty_result = s3_service.get_s3_config(
            bucket=DATA_INGESTION_BUCKET,
            key="test.yaml",
            domain="test_empty",
            s3_client=s3_client
        )
        
        assert empty_result == {}

def test_get_s3_config_exception(
    s3_client,
    mock_create_bucket,
    
):
    with pytest.raises(Exception) as e:
        
        s3_service.get_s3_config(
            bucket=DATA_INGESTION_BUCKET,
            key="anything.yaml",
            domain="testing",
            s3_client=s3_client
        )
            
    assert "NoSuchKey" in str(e)

def test_get_s3_object(
    s3_client,
    mock_create_bucket,
):

    s3_client.put_object(
        Bucket=DATA_INGESTION_BUCKET,
        Key="testing.yaml",
        Body="testing"
    )

    result = s3_service.get_s3_object(
        bucket=DATA_INGESTION_BUCKET,
        key="testing.yaml",
        s3_client=s3_client
    )

    assert result == b"testing"
    
    
def test_get_s3_object_exception(
    s3_client,
    mock_create_bucket
):
    with pytest.raises(Exception) as e:
        s3_service.get_s3_object(
            bucket=DATA_INGESTION_BUCKET,
            key="testing.yaml",
            s3_client=s3_client
        )
        
    assert "NoSuchKey" in str(e)
        
        