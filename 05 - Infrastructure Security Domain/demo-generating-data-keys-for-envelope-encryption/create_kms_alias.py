import json
import logging
import boto3
from botocore.exceptions import ClientError

# USE THIS EXACT LINE IF USING THE PLAYGROUND ACCOUNTS# USE THIS EXACT LINE IF USING THE PLAYGROUND ACCOUNTS
session = boto3.Session(profile_name="cloud_user", region_name="us-east-1")


# logger config
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
)

kms_client = session.client("kms")
ssm_client = session.client("ssm")

# Getting key id from parameter store.
ssm_parameter_raw = ssm_client.get_parameter(Name="key_id")
ssm_key_id = ssm_parameter_raw["Parameter"]["Value"]


def create_kms_key_alias(key_id, alias_name):
    """
    Creates a custom name/alias for a KMS key.
    """
    try:
        response = kms_client.create_alias(AliasName=alias_name, TargetKeyId=key_id)
    except ClientError:
        logger.exception("Could not create a key alias.")
        raise
    else:
        return response


if __name__ == "__main__":
    # Constants
    KEY_ID = ssm_key_id
    ALIAS_NAME = "alias/externalKey"
    logger.info("Creating a key alias...")
    kms = create_kms_key_alias(KEY_ID, ALIAS_NAME)
    logger.info("Key alias is created.")
