locals {
  bucket_prefix = "sooper-dooper-demo-"
  object_name   = "SooperSecretScript.sh"
}

resource "aws_kms_key" "s3key" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "bucket" {
  bucket_prefix = local.bucket_prefix
}

resource "aws_s3_bucket_object" "object_1" {
  bucket = aws_s3_bucket.bucket.id
  key    = local.object_name
  source = "./aws_sts.sh"
}
