#!/bin/bash

# THIS WILL FAIL
aws kms encrypt --key-id alias/externalKey --plaintext $(cat ./files/kms_details.txt | base64) --profile temp_cli --region us-east-1