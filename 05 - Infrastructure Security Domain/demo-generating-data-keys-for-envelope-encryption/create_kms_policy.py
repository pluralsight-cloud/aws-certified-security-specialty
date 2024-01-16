import json
import logging
import boto3
from botocore.exceptions import ClientError

# USE THIS EXACT LINE IF USING THE PLAYGROUND ACCOUNTS
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


def put_policy_kms_key(key_id, policy):
    """
    Attaches a key policy to the specified KMS key.
    """
    try:
        response = kms_client.put_key_policy(
            KeyId=key_id, PolicyName="default", Policy=policy
        )
    except ClientError:
        logger.exception("Could not attach a key policy.")
        raise
    else:
        return response


if __name__ == "__main__":
    # Constants
    KEY_ID = ssm_key_id
    # REPLACE ARN FOR PRINCIPAL
    POLICY = """
    {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "Allowing Access",
            "Effect": "Allow",
            "Principal": {"AWS": [
                "arn:aws:iam::000000000000:user/cloud_user"
            ]},
            "Action": "kms:*",
            "Resource": "*"
        }]
    }"""
    logger.info("Attaching a key policy...")
    kms = put_policy_kms_key(KEY_ID, POLICY)
    logger.info("Key policy is attached.")
