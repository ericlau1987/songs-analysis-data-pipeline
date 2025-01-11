resource "random_uuid" "uuid" {}

resource "aws_s3_bucket" "songs-analysis-data-pipeline-bucket" {
  bucket_prefix = "${var.project_name}-bucket-"
  force_destroy = true
  tags = {
    Name        = "Terraform"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "songs-analysis-data-pipeline-bucket-version" {
  bucket = aws_s3_bucket.songs-analysis-data-pipeline-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "block-s3-access" {
  bucket = aws_s3_bucket.songs-analysis-data-pipeline-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
