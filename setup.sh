# Setup script for the jenkins server
#aws configure set default.region eu-west-1
# Zip up the lambda function
zip jenkins-startup.zip jenkins-startup.py requirements.txt
# Create bucket for lambda function zip in Ireland
#aws s3api create-bucket --bucket jenkins-startup --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1 
# Put zip into bucket
aws s3 cp jenkins-startup.zip s3://jenkins-startup/jenkins-startup.zip
# Create secret in SSM
#aws ssm put-parameter --name "/github/webhook-secret" --type "SecureString" --value "$1"
aws cloudformation deploy --template-file cloud-template.yml --stack-name jenkins-stack --capabilities CAPABILITY_IAM --capabilities CAPABILITY_NAMED_IAM
sleep 10 # Sleep for 10 seconds so that container has been created before running task
aws ecs run-task --cluster ci-cd-cluster --task-definition jenkins-task --started-by start-jenkins-lambda --launch-type EC2