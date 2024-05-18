# API Gateway Construct

This package provides a construct for AWS Cloud Development Kit (CDK) to create an API Gateway with dynamic routes and methods based on a configuration.

## Features

- Creates an API Gateway with a custom name and description.
- Dynamically creates resources and methods based on a provided configuration.
- Supports Lambda integrations.

## Installation

To install this package, run the following command in your terminal:

```bash
pip install dscdk.apigateway
```

## Usage

```
from aws_cdk import App
from apigateway_construct import ApiGatewayStack

app = App()

lambda_stack = ...  # Your Lambda stack

config = {
    'routes': [
        {
            'path': '/myresource',
            'methods': ['GET'],
            'integration': 'lambda',
            'lambdaFunctionName': 'MyFunction',
        },
        # Add more routes as needed
    ],
}

ApiGatewayStack(app, "ApiGatewayStack", lambda_stack=lambda_stack, config=config)

app.synth()
```
