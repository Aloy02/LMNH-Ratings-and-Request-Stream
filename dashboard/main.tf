provider "aws" {
  region = var.AWS_REGION
}

# ------------------------------------------------------------------------------
# 1. Lookups for Existing VPC & Subnets
# ------------------------------------------------------------------------------

data "aws_vpc" "c26-vpc" {
  filter {
    name   = "tag:Name"
    values = [var.VPC_NAME]
  }
}

data "aws_subnet" "subnet" {
  filter {
    name   = "tag:Name"
    values = [var.SUBNET_1_NAME]
  }
}

# ------------------------------------------------------------------------------
# 2. Generate an RSA Private Key
# ------------------------------------------------------------------------------

resource "tls_private_key" "ec2_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# ------------------------------------------------------------------------------
# 3. Upload Public Key to AWS Key Pair
# ------------------------------------------------------------------------------

resource "aws_key_pair" "c26-aloysius-lmnh-pem" {
  key_name   = "c26-aloysius-lmnh-pem"
  public_key = tls_private_key.ec2_key.public_key_openssh
}

# ------------------------------------------------------------------------------
# 4. Save Private Key to a local .pem File
# ------------------------------------------------------------------------------
resource "local_file" "private_key" {
  content         = tls_private_key.ec2_key.private_key_pem
  filename        = "${path.module}/.pem"
  file_permission = "0400"
}

# ------------------------------------------------------------------------------
# 5. Security Group in the target VPC
# ------------------------------------------------------------------------------
resource "aws_security_group" "ec2_sg" {
  name        = "vpc-aloysius-lmnh-ec2-sg"
  description = "Allow SSH access from personal IP and unrestricted egress"
  vpc_id      = data.aws_vpc.c26-vpc.id

  ingress {
    description = "Allow SSH from Personal IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.PERSONAL_IP}/32"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "vpc-aloysius-lmnh-ec2-sg"
  }
}

# ------------------------------------------------------------------------------
# 6. Fetch the latest Amazon Linux 2023 AMI
# ------------------------------------------------------------------------------
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# ------------------------------------------------------------------------------
# 7. Launch the EC2 Instance with the Key Pair
# ------------------------------------------------------------------------------
resource "aws_instance" "ec2" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t3.micro"
  key_name                    = aws_key_pair.c26-aloysius-lmnh-pem.key_name
  subnet_id                   = data.aws_subnet.subnet.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "c26-aloysius-lmnh-ec2"
  }
}