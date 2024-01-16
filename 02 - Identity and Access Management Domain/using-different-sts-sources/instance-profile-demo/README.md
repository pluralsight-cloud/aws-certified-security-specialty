1. ssh -i %KEYNAME%.pem %EC2_DNS_OR_IP%
1. aws s3 ls
1. curl http://169.254.169.254/latest
1. Look at the instance security relevant info with `curl http://169.254.169.254/latest/dynamic/instance-identity`
1. You can see here there is a TON of instance specific meta data: `curl http://169.254.169.254/latest/meta-data`
1. We want to look for the profile being used and the credentials being used via `curl http://169.254.169.254/latest/meta-data/iam/security-credentials/SooperDooperS3FullAccess`
1. Then, test the AWS CLI call to view Amazon S3 buckets `aws s3 ls --region us-east-1`

## Get IAM Instance Profile

```bash
curl http://169.254.169.254/latest/meta-data/iam/info
```

Get Access Keys

```bash
curl http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance
```
