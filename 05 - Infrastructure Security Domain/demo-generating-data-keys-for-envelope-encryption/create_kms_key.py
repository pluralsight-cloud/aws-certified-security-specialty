import json
import logging
from datetime import date, datetime
import boto3
from botocore.exceptions import ClientError

# USE THIS EXACT LINE IF USING THE PLAYGROUND ACCOUNTS
session = boto3.Session(profile_name="cloud_user", region_name="us-east-1")


# AWS_REGION = "us-east-2"
# logger config
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
)
kms_client = session.client("kms")
ssm_client = session.client("ssm")


def json_datetime_serializer(obj):
    """
    Helper method to serialize datetime fields
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def create_kms_key():
    """
    Creates a unique customer managed KMS key and stores the ID in Parameter Store.
    """
    try:
        response = kms_client.create_key(
            Description="external-cmk",
            Tags=[{"TagKey": "Name", "TagValue": "external-cmk"}],
        )
        ssm_client.put_parameter(
            Name="key_id",
            Value=response["KeyMetadata"]["KeyId"],
            Description=response["KeyMetadata"]["Description"],
            Type="String",
            Overwrite=True,
        )
    except ClientError:
        logger.exception("Could not create a CMK key.")
        raise
    else:
        return response


if __name__ == "__main__":
    # Constants
    logger.info("Creating a symetric CMK...")
    kms = create_kms_key()
    logger.info(
        f"Symetric CMK is created with details: {json.dumps(kms, indent=4, default=json_datetime_serializer)}"
    )
