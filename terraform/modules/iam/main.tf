# resource "aws_iam_role_policy" "s3_bucket_policy" {
#   name = "s3_bucket_creation_policy"
#   role = iam_role.name.id

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Action = [
#           "s3:CreateBucket",
#           "s3:PutBucketPolicy",
#           "s3:PutBucketTagging"
#         ]
#         Resource = "arn:aws:s3:::songs-analysis-data-pipeline-bucket-*"
#       }
#     ]
#   })
# }

# # resource "aws_iam_role" "songs-analysis-data-pipeline-role" {
# #      name               = "songs-analysis-data-pipeline-role"
# #      assume_role_policy = jsonencode({
# #     Version = "2012-10-17"
# #     Statement = [
# #       {
# #         Action = "sts:AssumeRole"
# #         Effect = "Allow"
# #         Sid    = ""
# #         Principal = {
# #           Service = "ec2.amazonaws.com"
# #         }
# #       },
# #     ]
# #   })
# # }

# data "aws_iam_role" "songs-analysis-data-pipeline-role" {
#     arn = ""
# }

# resource "aws_iam_role_policy_attachment" "test-attach" {
#   role      = aws_iam_role.songs-analysis-data-pipeline-role.name
#   policy_arn = aws_iam_role_policy.s3_bucket_policy.arn
# }
