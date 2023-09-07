resource "aws_ecr_repository" "this" {
  name                 = "MusicBot"
  image_tag_mutability = "MUTABLE"

  force_delete = true

}