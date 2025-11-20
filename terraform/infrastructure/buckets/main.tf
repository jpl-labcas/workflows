

resource "aws_s3_bucket" "labcas-workflow-staging" {
      bucket = "labcas-${var.tenant}-${var.venue}-workflow-staging" # Replace with a globally unique bucket name
      tags = {
        tenant = var.tenant,
        venue = var.venue,
        application = "labcas",
        component = "workflow",
        createdBy : var.operator
      }

}

resource "aws_s3_bucket_acl" "labcas-workflow-staging" {
  bucket = aws_s3_bucket.labcas-workflow-staging.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "labcas-workflow-staging" {
  bucket = aws_s3_bucket.labcas-workflow-staging.id
  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_s3_bucket" "labcas-core-data-archive" {
  bucket = "labcas-${var.tenant}-${var.venue}-data-archive" # Replace with a globally unique bucket name
  tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "core",
    createdBy : var.operator
  }
}

resource "aws_s3_bucket_acl" "labcas-core-data-archive" {
  bucket = aws_s3_bucket.labcas-core-data-archive.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "labcas-core-data-archive" {
  bucket = aws_s3_bucket.labcas-core-data-archive.id
  versioning_configuration {
    status = "Enabled"
  }
}

