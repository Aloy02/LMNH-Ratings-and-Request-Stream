variable "AWS_REGION" {
  type        = string
  description = "AWS deployment region"
}

variable "VPC_NAME" {
  type        = string
  description = "Tag Name for target VPC"
}

variable "SUBNET_1_NAME" {
  type        = string
  description = "Tag Name for subnet 1"
}

variable "SUBNET_2_NAME" {
  type        = string
  description = "Tag Name for subnet 2"
}

variable "SUBNET_3_NAME" {
  type        = string
  description = "Tag Name for subnet 3"
}

variable "DB_USERNAME" {
  type        = string
  description = "Master username for database"
  sensitive   = true
}

variable "DB_PASSWORD" {
  type        = string
  description = "Master password for database"
  sensitive   = true
}

variable "PERSONAL_IP" {
  type        = string
  description = "Personal IP address for egress access"
  sensitive   = true
}

variable "TABLEAU_IP"{
  type        = string
  description = "IP address for Tableau access"
  sensitive   = true
}