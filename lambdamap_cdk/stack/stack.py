import os
import sys

from aws_cdk import core, aws_lambda, aws_ecr
from aws_cdk import core as cdk


class LambdaMapStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        """

        Parameters
        ----------
        folder : str, optional
            /path/to the folder containing the lambda function .py file
            (i.e. lambda.py) and Dockerfile.
        function_name : str, default="LambdaMapFunction"
            Name of the primary lambdamap function.
        memory_size : int, default=512
            Amount of memory allocated (in MB) to the lambdamap function.
        timeout_secs : int, default=900
            Max. amount of time (in seconds) the lambdamap function will run
            before stopping.

        """
        super().__init__(scope, construct_id)

        folder = kwargs.get("folder", None)

        if folder is None:
            folder = os.path.dirname(os.path.realpath(__file__))

        function_name = kwargs.get("function_name", "LambdaMapFunction")
        memory_size = kwargs.get("memory_size", 512) 
        timeout_secs = kwargs.get("timeout_secs", 900) 
        extra_cmds = kwargs.get("extra_cmds", None)

        if extra_cmds is None:
            build_args = None
        else:
            build_args = {"EXTRA_CMDS": extra_cmds}

        ecr_image = \
            aws_lambda.EcrImageCode \
                      .from_asset_image(directory=folder,
                                        build_args=build_args)

        lambda_function = aws_lambda.Function(
            self, 
            id=function_name,
            description="LambdaMap",
            code=ecr_image,
            handler=aws_lambda.Handler.FROM_IMAGE,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            function_name=function_name,
            memory_size=memory_size,
            timeout=core.Duration.seconds(timeout_secs)
        )

        return
