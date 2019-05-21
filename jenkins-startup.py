import boto3
import hmac
import logging
import json
from  datetime import datetime, timedelta

def validate_request(event):
    logging.info("Received event: " + json.dumps(event, indent=2))
    client = boto3.client('ssm')
    param_rsp = client.get_parameter(Name='github/webhook-secret', WithDecryption=True)
    secret_token = param_rsp['Parameter']['Value']
    signature = 'sha1=' + hmac.digest(secret_token, event['body'], 'sha1')
    if not hmac.compare_digest(signature, event['X_HUB_SIGNATURE']):
        raise Exception('Invalid signature')

def create_timer():
    stop_time = datetime.now() + timedelta(hours=1)
    stop_expression = stop_time.strftime('cron(%M %H %d %m ? %Y')
    client = boto3.client('events')
    client.put_role(
        Name='stop-jenkins',
        ScheduleExpression=stop_expression
    )

def lambda_function(event, context):
    #validate_request(event)

    client = boto3.client('ecs')
    running_tasks = client.list_tasks(
                        cluster='ci-cd-cluster',
                        startedBy='start-jenkins-lambda',
                        desiredStatus='RUNNING'
                    )

    if not running_tasks['taskArns']:
        ec2_client = boto3.client('ec2')

        ec2_client.run_instances(
            LaunchTemplate={
                'LaunchTemplateName': 'jenkins-ec2-instance'
            }
        )

        client.run_task(
            cluster='ci-cd-cluster',
            taskDefinition='jenkins-task',
            count=1,
            launchType='EC2',
            startedBy='start-jenkins-lambda'
        )

    # Update cloudwatch event schedule to stop ecs task
    create_timer()


def stop_jenkins(event, context):
    client = boto3.client('ecs')
    jenkins_instance = client.list_tasks(
        cluster='ci-cd-cluster',
        startedBy='start-jenkins-lambda',
        desiredStatus='RUNNING'
    )

    if len(jenkins_instance['taskArns']) != 0:
        jenkins_arn = jenkins_instance['taskArns'][0]

        ec2_client = boto3.client('ec2')
        ec2_client.stop_instances(
            
        )

        client.stop_task(
            cluster='ci-cd-cluster',
            task=jenkins_arn
        )





