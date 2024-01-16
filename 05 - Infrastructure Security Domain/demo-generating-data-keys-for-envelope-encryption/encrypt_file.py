import base64
import json
import logging
import boto3
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

# USE THIS EXACT LINE IF USING THE PLAYGROUND ACCOUNTS
session = boto3.Session(profile_name="cloud_user", region_name="us-east-1")


# logger config
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
)
kms_client = session.client("kms")


def create_data_key(key_alias, key_spec="AES_256"):
    """
    Generates a unique symmetric data key for client-side encryption.
    """
    try:
        response = kms_client.generate_data_key(KeyId=key_alias, KeySpec=key_spec)
    except ClientError as e:
        logging.error(e)
        return None, None
    # Return the encrypted and plaintext data key
    return response["CiphertextBlob"], base64.b64encode(response["Plaintext"])


def encrypt_file(filename, key_alias):
    """
    Encrypts plaintext into ciphertext by using a KMS key.
    """
    # Read the entire file into memory
    try:
        with open(filename, "rb") as file:
            file_contents = file.read()
    except IOError as e:
        logging.error(e)
        return False
    data_key_encrypted, data_key_plaintext = create_data_key(key_alias)
    if data_key_encrypted is None:
        return False
    logging.info("Created new AWS KMS data key")
    logging.info(f"Here is the plaintext key material => {data_key_plaintext}")
    # Encrypt the file
    f = Fernet(data_key_plaintext)
    file_contents_encrypted = f.encrypt(file_contents)
    # Write the encrypted data key and encrypted file contents together
    try:
        with open(filename + ".encrypted", "wb") as file_encrypted:
            file_encrypted.write(
                len(data_key_encrypted).to_bytes(NUM_BYTES_FOR_LEN, byteorder="big")
            )
            file_encrypted.write(data_key_encrypted)
            file_encrypted.write(file_contents_encrypted)
            logging.info(
                "Combined encrypted data key and file contents into single file."
            )
    except IOError as e:
        logging.error(e)
        return False
    except ClientError:
        logger.exception("Could not encrypt the file.")
        raise
    else:
        return True


if __name__ == "__main__":
    # Constants
    FILE_NAME = "./files/kms_details.txt"
    KEY_ALIAS = "alias/externalKey"
    NUM_BYTES_FOR_LEN = 4
    logger.info("Encrypting file...")
    kms = encrypt_file(FILE_NAME, KEY_ALIAS)
    logger.info(f"Encrypted file: {kms}.")
