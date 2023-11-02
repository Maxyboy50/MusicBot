data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }

}
resource "aws_iam_role" "execution_role" {
  name               = "ecsrole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json

}

data "aws_iam_policy_document" "task_policy_document" {
  statement {
    effect = "Allow"
    actions = ["ecs:ExecuteCommand",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [aws_cloudwatch_log_group.this.arn, "${aws_cloudwatch_log_group.this.arn}:log-stream:ecs/musicbot/*", data.aws_ecr_repository.this.arn]
  }
  statement {
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

}



resource "aws_iam_policy" "task_policy" {
  name        = "music_bot_policy"
  description = "Music Bot task policy to allow writes to cloud watch logs"
  policy      = data.aws_iam_policy_document.task_policy_document.json
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.task_policy.arn
}
# ecs execution role


# ecs task role
#   - cloudwatch logs

