variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "model_bucket_name" {
  type    = string
  default = "sensor-model-sv2"
}

variable "aws_account_id" {
  type    = string
  default = "975050177947"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}

