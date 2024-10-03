import time

import boto3
import requests

LOCALSTACK_HOST = "https://localhost.localstack.cloud:4566"
STACK_NAME = "WordpressStack"


def client(service: str):
    return boto3.client(service, endpoint_url=LOCALSTACK_HOST)


def retry(function: callable, retries=3, sleep=1.0, sleep_before=0, **kwargs):
    raise_error = None
    if sleep_before > 0:
        time.sleep(sleep_before)
    retries = int(retries)
    for i in range(0, retries + 1):
        try:
            return function(**kwargs)
        except Exception as error:
            raise_error = error
            time.sleep(sleep)
    raise raise_error


def test_wordpress_status_code():
    cloudformation = client("cloudformation")

    stack_info = cloudformation.describe_stacks(StackName=STACK_NAME)["Stacks"][0]
    wp_endpoint = stack_info["Outputs"][0]["OutputValue"]
    wp_url = f"http://{wp_endpoint}:4566"

    def _assert_wp_response():
        result = requests.get(wp_url)

        assert result.status_code == 200
        assert "WordPress" in result.text

    retry(_assert_wp_response, sleep=2)
