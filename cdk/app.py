#!/usr/bin/env python3
from aws_cdk import core as cdk
from stack.stack import LambdaMapStack


if __name__ == '__main__':
    app = cdk.App()
    LambdaMapStack(app, "LambdaMapStack")
    app.synth()
