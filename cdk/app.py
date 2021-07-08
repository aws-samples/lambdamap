#!/usr/bin/env python3
"""

$ cdk deploy --context \
    stack_name=LambdaMapStack \
    function_name=LambdaMapFunction \
    memory_size=512 \
    timeout_secs=900

"""
from aws_cdk import core as cdk
from stack.stack import LambdaMapStack


if __name__ == '__main__':
    app = cdk.App()

    stack_name = app.node.try_get_context("stack_name")
    function_name = app.node.try_get_context("function_name")
    memory_size = app.node.try_get_context("memory_size")
    timeout_secs = app.node.try_get_context("timeout_secs")

    if stack_name is None:
        stack_name = "LambdaMapStack"
    if function_name is None:
        function_name = "LambdaMapFunction"
    if memory_size is None:
        memory_size = 512
    if timeout_secs is None:
        timeout_secs = 900

    kwargs = dict(stack_name=stack_name, function_name=function_name,
                  memory_size=memory_size, timeout_secs=timeout_secs)

    LambdaMapStack(app, stack_name, **kwargs)

    app.synth()
