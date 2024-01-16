# Look up the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]
  }
}

# Create the IAM Role
resource "aws_iam_role" "SooperDooperS3AccessInstanceRole" {
  name               = "SooperDooperS3AccessInstanceRole"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Create the IAM instance profile
resource "aws_iam_instance_profile" "SooperDooperS3AccessInstanceRole" {
  name = "SooperDooperS3AccessInstanceRole"
  role = aws_iam_role.SooperDooperS3AccessInstanceRole.name
}

# Attach the AmazonS3FullAccess policy to the IAM instance profile
resource "aws_iam_role_policy_attachment" "SooperDooperS3AccessInstanceRole" {
  role       = aws_iam_instance_profile.SooperDooperS3AccessInstanceRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Create the EC2 instances
resource "aws_instance" "my_ec2_instances" {
  count = 3

  # Attach the IAM instance profile to the EC2 instances
  iam_instance_profile = aws_iam_instance_profile.SooperDooperS3AccessInstanceRole.name

  # Use the latest Amazon Linux 2 AMI for the EC2 instances
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro"
}
