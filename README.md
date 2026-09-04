[![LocalStack Pods Launchpad](https://localstack.cloud/gh/launch-pod-badge.svg)](https://app.localstack.cloud/launchpad?url=https://github.com/localstack-samples/wordpress-ecs-rds-cdk/releases/download/latest/release-pod.zip)
[![GitHub Actions](https://github.com/localstack-samples/wordpress-ecs-rds-cdk/actions/workflows/integration-test.yml/badge.svg)](https://github.com/localstack-samples/wordpress-ecs-rds-cdk/actions/workflows/integration-test.yml)

## Wordpress Sample

Wordpress deployed using ECS and RDS


## Quickstart

This sample requires a valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/aws/getting-started/auth-token/) to activate LocalStack.

To install python requirements and developer tools (the [`lstk` CLI](https://docs.localstack.cloud/aws/developer-tools/running-localstack/lstk/), which also requires the AWS CLI) into a venv run:

    make install

Start LocalStack for AWS with the `LOCALSTACK_AUTH_TOKEN` pre-configured:

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
```

Then, to deploy the CDK app:

    make deploy-local

## Tinker

After running `make install`, when you activate the virtual environment with

    source .venv/bin/activate

you can use the `lstk` proxies for the AWS CDK and AWS CLIs:

    lstk cdk
    lstk aws

You can for example get the name of the bucket that was created and whose name was added as an SSM parameter:

    lstk aws ssm get-parameter --name /artifacts/bucket

Or list the created lambdas:

    lstk aws lambda list-functions
