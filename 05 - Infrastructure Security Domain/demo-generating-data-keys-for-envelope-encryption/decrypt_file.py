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


def decrypt_data_key(data_key_encrypted):
    """
    Decrypts an encrypted data key.
    """
    # Decrypt the data key
    try:
        response = kms_client.decrypt(CiphertextBlob=data_key_encrypted)
    except ClientError as e:
        logging.error(e)
        return None
    # Return plaintext base64-encoded binary data key
    return base64.b64encode((response["Plaintext"]))


def decrypt_file(filename):
    """
    Decrypts a file encrypted by encrypt_file() by using a KMS key.
    """
    # Read the encrypted file into memory
    try:
        with open(filename + ".encrypted", "rb") as file:
            file_contents = file.read()
    except IOError as e:
        logging.error(e)
        return False
    data_key_encrypted_len = (
        int.from_bytes(file_contents[:NUM_BYTES_FOR_LEN], byteorder="big")
        + NUM_BYTES_FOR_LEN
    )
    data_key_encrypted = file_contents[NUM_BYTES_FOR_LEN:data_key_encrypted_len]
    # Decrypt the data key before using it
    data_key_plaintext = decrypt_data_key(data_key_encrypted)
    if data_key_plaintext is None:
        logging.error("Cannot decrypt the data key.")
        return False
    # Decrypt the rest of the file
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents[data_key_encrypted_len:])
    # Write the decrypted file contents
    try:
        with open(filename, "wb") as file_decrypted:
            file_decrypted.write(file_contents_decrypted)
    except IOError as e:
        logging.error(e)
        return False
    except ClientError:
        logger.exception("Could not decrypt the file.")
        raise
    else:
        return True


if __name__ == "__main__":
    # Constants
    FILE_NAME = "./files/kms_details.txt"
    NUM_BYTES_FOR_LEN = 4
    logger.info("Decrypting file...")
    kms = decrypt_file(FILE_NAME)
    logger.info(f"Decrypted file: {kms}.")
