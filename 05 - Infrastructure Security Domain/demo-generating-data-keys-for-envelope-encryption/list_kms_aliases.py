import json
import logging
from datetime import date, datetime
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


def json_datetime_serializer(obj):
    """
    Helper method to serialize datetime fields
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def list_kms_aliases(key_id, max_items):
    """
    Gets a list of aliases of a KMS key.
    """
    try:
        # creating paginator object for list_aliases() method
        paginator = kms_client.get_paginator("list_aliases")
        # creating a PageIterator from the paginator
        response_iterator = paginator.paginate(
            KeyId=key_id, PaginationConfig={"MaxItems": max_items}
        )
        full_result = response_iterator.build_full_result()
        aliases_list = []
        for page in full_result["Aliases"]:
            aliases_list.append(page)
    except ClientError:
        logger.exception("Could not list KMS aliases.")
        raise
    else:
        return aliases_list


if __name__ == "__main__":
    # Constants
    # FAKE KEY_ID - Replace this with yours
    KEY_ID = "001191e0-89a2-4949-99a1-fd952531c988"
    MAX_ITEMS = 10
    logger.info("Getting KMS key aliases...")
    kms_aliases = list_kms_aliases(KEY_ID, MAX_ITEMS)
    for kms_alias in kms_aliases:
        logger.info(
            f"Key Alias Details: {json.dumps(kms_alias, indent=4, default=json_datetime_serializer)}"
        )
