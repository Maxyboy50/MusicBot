resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "MusicBot VPC"
  }
}
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
}
# resource "aws_route_table_association" "igw" {
#   gateway_id     = aws_internet_gateway.this.id
#   route_table_id = aws_vpc.this.default_route_table_id
# }
resource "aws_route" "egress" {
  route_table_id         = aws_vpc.this.default_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}
resource "aws_route_table_association" "subnet_1" {
  subnet_id      = aws_subnet.subnet_1.id
  route_table_id = aws_vpc.this.default_route_table_id
}
resource "aws_route_table_association" "subnet_2" {
  subnet_id     = aws_subnet.subnet_2.id
  route_table_id = aws_vpc.this.default_route_table_id
}
resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-2a"

}

resource "aws_subnet" "subnet_2" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-2b"

}

resource "aws_security_group" "this" {
  name        = "allow http traffic"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.this.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "HTTP"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http"
  }
}
# security group
# Route Table
# Access Control List
# Internet Gateway - need for public subnet
# vpc
# Subnet