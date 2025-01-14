module "s3bucket" {
  source = "./modules/s3"
  project_name = local.PROJECT_NAME
}
