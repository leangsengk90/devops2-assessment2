# Remote state data source to get infrastructure outputs
data "terraform_remote_state" "infrastructure" {
  # backend = "local"
  # config = {
  #   path = "../../infrastructures/terraform.tfstate.d/${terraform.workspace}/terraform.tfstate"
  # }

  # Optional: Configure remote state backend
  backend = "s3"
  config = {
    bucket = "devops2-g4-remote-state"
    key    = "env:/${terraform.workspace}/infrastructures/terraform.tfstate"
    region = "us-east-1"
  }
}