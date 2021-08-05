#!/usr/bin/env python3
"""

$ cdk deploy --context \
    stack_name=LambdaMapStack \
    function_name=LambdaMapFunction \
    memory_size=512 \
    timeout_secs=900

"""
import os

from aws_cdk import core
from stack.stack import LambdaMapStack


if __name__ == '__main__':
    app = core.App()

    folder = app.node.try_get_context("folder")
    stack_name = app.node.try_get_context("stack_name")
    function_name = app.node.try_get_context("function_name")
    memory_size = app.node.try_get_context("memory_size")
    timeout_secs = app.node.try_get_context("timeout_secs")
    extra_cmds = app.node.try_get_context("extra_cmds")

    if stack_name is None:
        stack_name = "LambdaMapStack"
    if function_name is None:
        function_name = "LambdaMapFunction"
    if memory_size is None:
        memory_size = 256
    if timeout_secs is None:
        timeout_secs = 900

    kwargs = dict(stack_name=stack_name, function_name=function_name,
                  memory_size=int(memory_size), timeout_secs=int(timeout_secs),
                  folder=folder, extra_cmds=extra_cmds)

    LambdaMapStack(app, stack_name,
        env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                             region=os.getenv('CDK_DEFAULT_REGION')), **kwargs)

    app.synth()
