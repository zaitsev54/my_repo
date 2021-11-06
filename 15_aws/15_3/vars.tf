variable "aws_region" {
  description = "AWS region to launch servers."
  default     = "us-east-2"
}

variable "aws_amis" {
  default = {
    us-east-2 = "ami-fcc19b99"
  }
}
