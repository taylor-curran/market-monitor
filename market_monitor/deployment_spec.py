
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner

DeploymentSpec(
    name="my-first-deployment",
    flow_location="./first_flow.py",
    flow_name="Get User Data from Twitter API",
    parameters={
        'BEARER_TOKEN': 'TWITTER_BEARER_TOKEN',
        'users':[
            'apacheairflow', 
            'astronomerio'
            ],
            'fields': 'public_metrics'
        },
    tags=['Twitter_API'],
    flow_runner=SubprocessFlowRunner(),
    flow_storage='e4ccba6c-01d8-42c1-a3d7-4eb0ec9d41e2'
)
