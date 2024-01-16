#!/bin/bash
aws sts assume-role --role-arn arn:aws:iam::%ACCOUNT_ID%:role/SooperDooperEc2AdminRole --role-session-name `echo $RANDOM | base64 | head -c 20; echo` --profile cloud_user