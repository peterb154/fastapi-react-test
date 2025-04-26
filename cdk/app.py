import aws_cdk as cdk

from stacks.app_stack import AppStack

project_name = "fasthml-react-test"

app = cdk.App()
AppStack(app, f"{project_name}-app")

app.synth()
