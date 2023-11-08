resource "aws_cloudwatch_log_group" "this" {
  name              = "MusicBotLogs"
  retention_in_days = 1
} 