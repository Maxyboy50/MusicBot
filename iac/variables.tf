variable "music_bot_token" {
  type        = string
  description = "Bot token to be used"
}


variable "subnets" {
  type = map(object({
    cidr_block        = string
    availability_zone = string
  }))
  default     = {}
  description = "Variable that will be looped over when creating subnets, can contain all necessary subnet attributes"

}