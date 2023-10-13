resource "aws_ecs_cluster" "this" {
  name = "MusicBot"

}

resource "aws_ecs_cluster_capacity_providers" "this" {
  cluster_name       = aws_ecs_cluster.this.name
  capacity_providers = ["FARGATE"]

  default_capacity_provider_strategy {
    base              = 0
    weight            = 100
    capacity_provider = "FARGATE"
  }
}
resource "aws_ecs_task_definition" "this" {
  family                   = "service"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.execution_role.arn
  task_role_arn            = aws_iam_role.execution_role.arn
  network_mode             = "awsvpc"
  container_definitions = jsonencode([
    {
      name      = "musicbot"
      image     = "912434042761.dkr.ecr.us-east-2.amazonaws.com/testrepo"
      cpu       = 1024
      memory    = 2048
      essential = true
      environment : [
        {
          "name" : "MUSIC_BOT_TOKEN",
          "value" : "${var.music_bot_token}"
        }
      ]
      logConfiguration : {
        "logDriver" : "awslogs"
        options : {
          "awslogs-group" : "/ecs/MusicBot",
          "awslogs-region" : "us-east-2",
          "awslogs-stream-prefix" : "ecs"
        }
  } }])
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }
}
resource "aws_ecs_service" "willie_neal" {
  name            = "MusicBot"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  depends_on      = [aws_iam_role.execution_role]
  network_configuration {
    security_groups  = ["sg-07efeac40c79e8a1c"]
    assign_public_ip = true
    subnets          = ["subnet-096989484e460a3ba", "subnet-018a9c920ac2d8e86", "subnet-03ada96d0c0254536"]
  }

}
# task definition
# - where networking is defined

# ecs service
