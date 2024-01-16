import os
import boto3
import logging

# setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Retrieve the access key and secret key from environment variables
access_key = os.environ["AWS_ACCESS_KEY_ID"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
session_token = os.environ["AWS_SESSION_TOKEN"]
aws_region = os.getenv("AWS_DEFAULT_REGION", default="us-east-1")


# Create an EC2 client
ec2 = boto3.client(
    "ec2",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=aws_region,
    aws_session_token=session_token,
)

# Creating an STS client to show the assumed identity
sts = boto3.client(
    "sts",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=aws_region,
    aws_session_token=session_token,
)

# Get a list of all running EC2 instances
instances = ec2.describe_instances(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
)

# Showing the STS identity
identity = sts.get_caller_identity()
print(f'\nWe are currently using this identity: {identity["Arn"]}')

# Shut down each instances if there are any, else it shows a None Found sign.
if instances["Reservations"]:
    instances = instances["Reservations"][0]["Instances"]
    print(f"We found {len(instances)} running in the account!")
    for instance in instances:
        print(f'Shutting down the following instance: {instance["InstanceId"]}')
        ec2.stop_instances(InstanceIds=[instance["InstanceId"]])
else:
    print(
        """
 ____________________
/                    \\
!      None Found    !
\____________________/
         !  !
         !  !
         L_ !
        / _)!
       / /__L
 _____/ (____)
        (____)
 _____  (____)
      \_(____)
         !  !
         !  !
         \__/
"""
    )
