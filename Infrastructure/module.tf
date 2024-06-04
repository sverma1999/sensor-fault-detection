terraform {
  backend "s3" {
    bucket  = "sfd-tf-state-bucket"
    key     = "key/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = "us-east-1"
  # region = lookup(env, "AWS_REGION")
}

module "sensor_ec2" {
  source = "./sensor_ec2"
}

# module "sensor_model" {
#   source = "./sensor_model_bucket"
#   providers = {
#     aws = aws
#   }
# }

module "sensor_ecr" {
  source = "./sensor_ecr"
}

# module "sensor_pred_data" {
#   source = "./sensor_pred_data_bucket"
#   providers = {
#     aws = aws
#   }
# }
