resource "aws_ecr_repository" "this" {
  name                 = "musicbot"
  image_tag_mutability = "MUTABLE"

  force_delete = true

}
