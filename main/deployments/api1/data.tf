# Remote state data source to get infrastructure outputs
data "terraform_remote_state" "infrastructure" {
  backend = "local"

  config = {
    path = "../../infrastructures/terraform.tfstate.d/${terraform.workspace}/terraform.tfstate"
  }
}
