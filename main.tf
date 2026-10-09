provider "aws" {
  region = var.AWS_REGION
}

# ------------------------------------------------------------------------------
# 1. Lookups for Existing VPC & Subnets & EC2 Instance
# ------------------------------------------------------------------------------
data "aws_vpc" "c26-vpc" {
  filter {
    name   = "tag:Name"
    values = [var.VPC_NAME]
  }
}

data "aws_subnet" "subnet_1" {
  filter {
    name   = "tag:Name"
    values = [var.SUBNET_1_NAME]
  }
}

data "aws_subnet" "subnet_2" {
  filter {
    name   = "tag:Name"
    values = [var.SUBNET_2_NAME]
  }
}

data "aws_subnet" "subnet_3" {
  filter {
    name   = "tag:Name"
    values = [var.SUBNET_3_NAME]
  }
}

data "aws_instance" "existing_ec2" {
  filter {
    name   = "tag:Name"
    values = ["c26-aloysius-lmnh-ec2"]
  }

  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.c26-vpc.id]
  }
}

# ------------------------------------------------------------------------------
# 2. Subnet Group
# ------------------------------------------------------------------------------
resource "aws_db_subnet_group" "c26-aloysius-lmnh-subnet-group" {
  name       = "c26-aloysius-lmnh-subnet-group"
  subnet_ids = [
    data.aws_subnet.subnet_1.id,
    data.aws_subnet.subnet_2.id,
    data.aws_subnet.subnet_3.id
  ]

  tags = {
    Name = "c26-aloysius-lmnh-subnet-group"
  }
}

# ------------------------------------------------------------------------------
# 3. Security Group
# ------------------------------------------------------------------------------
resource "aws_security_group" "c26-aloysius-lmnh-db-sg" {
  name        = "c26-aloysius-lmnh-db-sg"
  description = "Security group for the database"
  vpc_id      = data.aws_vpc.c26-vpc.id

  ingress {
    description = "Allow specific inbound PostgreSQL access within VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [
      "${var.PERSONAL_IP}/32",
      "${data.aws_instance.existing_ec2.private_ip}/32",
      "${var.TABLEAU_IP}"
    ]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ------------------------------------------------------------------------------
# 4. Database Instance
# ------------------------------------------------------------------------------
resource "aws_db_instance" "lmnh-db" {
  identifier        = "c26-aloysius-lmnh-db"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = "museum"
  username = var.DB_USERNAME
  password = var.DB_PASSWORD

  # Network Links
  db_subnet_group_name   = aws_db_subnet_group.c26-aloysius-lmnh-subnet-group.name
  vpc_security_group_ids = [aws_security_group.c26-aloysius-lmnh-db-sg.id]
  publicly_accessible    = true

  skip_final_snapshot = true
}