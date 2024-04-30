import aws_cdk as cdk
from wordpress import WordpressStack


def main():
    app = cdk.App()

    WordpressStack(app, "WordpressStack")

    app.synth()


if __name__ == "__main__":
    main()
