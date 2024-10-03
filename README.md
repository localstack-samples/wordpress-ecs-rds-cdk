[![LocalStack Pods Launchpad](https://localstack.cloud/gh/launch-pod-badge.svg)](https://app.localstack.cloud/launchpad?url=https://github.com/localstack-samples/wordpress-ecs-rds-cdk/releases/download/latest/release-pod.zip
[![GitHub Actions](https://github.com/localstack-samples/wordpress-ecs-rds-cdk/actions/workflows/integration-test.yml/badge.svg)](https://github.com/localstack-samples/wordpress-ecs-rds-cdk/actions/workflows/integration-test.yml)
wordpress-ecs-rds-cdk
===============================

Wordpress deployed using ECS and RDS


## Quickstart

to install python requirements and developer tools (ckdlocal, awslocal) into a venv run:

    make install

then, to deploy the cdk app, first start localstack and run

    make deploy-local

## Tinker

After running `make install`, when you activate the virtual environment with

    source .venv/bin/activate

you get the *local commands:

    cdklocal
    awslocal

You can for example get the name of the bucket that was created and whose name was added as an SSM parameter:

    awslocal ssm get-parameter --name /artifacts/bucket

Or list the created lambdas:

    awslocal lambda list-functions
