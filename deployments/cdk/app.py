import aws_cdk as cdk
import env
from wordpress import WordpressStack


def main():
    app = cdk.App()

    WordpressStack(app, "WordpressStack", env=env.ENV_LOCAL)

    app.synth()


if __name__ == "__main__":
    main()
