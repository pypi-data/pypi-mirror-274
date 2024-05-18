# lambda_stack.py
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)

class MultiLambdaStack(Construct):
    @property
    def lambda_functions(self):
        """Return the dictionary of Lambda functions."""
        return self._lambda_functions
    
    def __init__(self, scope: Construct, id: str, config: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a dictionary to hold the Lambda functions
        self._lambda_functions = {}

        # Define a User Lambda function
        self._lambda_functions['userFunction'] = _lambda.Function(self, 'userFunction',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="hello.handler",
            code=_lambda.Code.from_asset(f"lambda")
        )

        # Define a Group Lambda function
        self._lambda_functions['groupFunction'] = _lambda.Function(self, 'groupFunction',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="hello.handler",
            code=_lambda.Code.from_asset(f"lambda")
        )

        # Define a Car Lambda function
        self._lambda_functions['carFunction'] = _lambda.Function(self, 'carFunction',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="hello.handler",
            code=_lambda.Code.from_asset(f"lambda")
        )