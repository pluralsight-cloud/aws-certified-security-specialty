#!/bin/bash

# Getting arguments for making correct AWS Account call
# a: AWS Account
# r: Role Arn
while getopts a:r: flag
do
    case "${flag}" in
        a) account=${OPTARG};;
        r) role_name=${OPTARG};;
    esac
done
echo "AWS Account: $account";
echo "IAM Role Name: $role_name";

ROLE_ARN="arn:aws:iam::${account}:role/${role_name}"

aws sts assume-role --role-arn $ROLE_ARN --role-session-name `echo $RANDOM | base64 | head -c 20; echo`