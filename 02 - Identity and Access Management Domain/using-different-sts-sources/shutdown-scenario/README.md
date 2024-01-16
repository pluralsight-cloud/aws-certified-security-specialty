# High-level Steps

1. Generate temporary credentials locally via the aws_sts.sh script.
1. export those values manually for now.
1. Run `aws sts get-caller-identity` to verify which role is being used.

## Show current user

```bash
aws sts get-caller-identity --profile cloud_user
```

## Generate Temp Credentials

```bash
aws sts assume-role --role-arn arn:aws:iam::%ACCOUNT ID%:role/SooperDooperEc2AdminRole --role-session-name `echo $RANDOM | base64 | head -c 20; echo` --profile cloud_user
```

## Export values if testing

```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=
```
