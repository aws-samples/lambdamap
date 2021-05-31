import os

from aws_cdk import core, aws_lambda, aws_ecr
from aws_cdk import core as cdk

PWD = os.path.dirname(os.path.realpath(__file__))


class LambdaMapStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        """
        """
        super().__init__(scope, construct_id, **kwargs)

        ecr_image = aws_lambda.EcrImageCode.from_asset_image(directory=PWD)

        lambda_function = aws_lambda.Function(self, 
          id            = "LambdaMapFunction",
          description   = "LambdaMap",
          code          = ecr_image,
          handler       = aws_lambda.Handler.FROM_IMAGE,
          runtime       = aws_lambda.Runtime.FROM_IMAGE,
          function_name = "LambdaMapFunction",
          memory_size   = 512,
          timeout       = core.Duration.minutes(15),
        )
