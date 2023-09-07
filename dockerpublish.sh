
ACCOUNTID=$(aws sts get-caller-identity --query Account | tr -d '"')


REPOSITORYURI=$(aws ecr describe-repositories --query "repositories[0].repositoryUri" | tr -d '"')


aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $ACCOUNTID.dkr.ecr.us-east-2.amazonaws.com

sudo docker build -t $ACCOUNTID:latest .

sudo docker push $REPOSITORYURI:latest

