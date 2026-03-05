[![LocalStack Pods Launchpad](https://localstack.cloud/gh/launch-pod-badge.svg)](https://app.localstack.cloud/launchpad?url=https://github.com/localstack-samples/wordpress-ecs-rds-cdk/releases/download/latest/release-pod.zip)
[![GitHub Actions](https://github.com/localstack-samples/wordpress-ecs-rds-cdk/actions/workflows/integration-test.yml/badge.svg)](https://github.com/localstack-samples/wordpress-ecs-rds-cdk/actions/workflows/integration-test.yml)

## Wordpress Sample

Wordpress deployed using ECS and RDS


## Quickstart

This sample requires a valid [LocalStack for AWS license](https://localstack.cloud/pricing). Your license provides a [`LOCALSTACK_AUTH_TOKEN`](https://docs.localstack.cloud/getting-started/auth-token/) to activate LocalStack.

To install python requirements and developer tools (cdklocal, awslocal) into a venv run:

    make install

Start LocalStack Pro with the `LOCALSTACK_AUTH_TOKEN` pre-configured:

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
make start
make ready
```

Then, to deploy the CDK app:

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
