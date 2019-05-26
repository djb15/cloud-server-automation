# Cloud Server Automation
This repository forms part of my dissertation at Cranfield University for MSc Global Product Development and Management.  The title of the dissertation is "Cloud Cost Reduction in Consumer Facing Tech Startups".

The code in this repo is a demonstration of cost reduction in the cloud.  It involves running a Jenkins server in AWS, with Lambda functions and CloudWatch event rules that automate server startup and shutdown to minimise EC2 costs.

## What the demo does
The demo is an example of how to reduce costs in the cloud by automating server lifetime.  For this example the Jenkins server is turned on from activity in GitHub, and is set to switch off 1 hour after the last GitHub activity.  This involves setting up a webhook from GitHub to trigger the Lambda which is outside the scope of the demo and is left as an exercise to the interested reader.

To simplify the demonstration I've provided a script that mimics activity from a GitHub repository.  Instruction on how to run the demo are below.

## Prerequisites
This demo requires the following tools to be installed:

- **AWS CLI**

After installing AWS CLI run ```aws configure``` to setup the CLI to use your AWS account.

## Running the demo
Follow these steps to exectute the demo:

1. ```./setup.sh```

   This shell script sets the default AWS region to eu.west.1 (Ireland), zips up the Lambda function, creates an S3 bucket on AWS, uploads the zip to the bucket, deploys the CloudFormation stack and then starts the Jenkins task.
2. ```./github_activity.sh```

   This shell scripts mimics activity from GitHub by invoking the Lambda function.  It creates a file called `activity.log` in the current directory with the ID of the instance running Jenkins.  Copy this ID.  It will be referred to as \<ID\> below.
3. ```./get_instance_ip.sh <ID>```

   This shell script returns the public IP address of the running Jenkins instance. An example execution looks like `./get_instance_ip.sh i-0f1904dbb435ee275`, using the ID copied from the previous step as an input parameter. Paste the returned value into your browser to see the demo in action.  Visiting this IP after an hour should not work, since the Jenkins server should have been automatically switched off.

**NOTE**: If you do not have permission to execute any of the shell scripts run the following command: `chmod 700 *.sh`

## Cleaning Up
After running the demo, you should clear up the CloudFormation stack by running:

* `./teardown.sh`

This will delete everything but an S3 bucket containing the zip of the lambda function.  Delete this by logging in to the AWS S3 console and performing a manual deletion.




