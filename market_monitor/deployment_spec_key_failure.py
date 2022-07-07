
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner
from dotenv import load_dotenv
import os

DeploymentSpec(
    name="twitter-user-query-flow-FAILURE-EXPIRED-KEY",
    flow_location="./twitter_user_query_flow.py",
    flow_name="Get User Data from Twitter API",
    parameters={
        'TWITTER_BEARER_TOKEN': 'EXPIRED_TWITTER_BEARER_TOKEN',
        'users':[
            'apacheairflow', 
            'astronomerio'
            ],
            'fields': 'public_metrics'
        },
    tags=['Twitter_API'],
    flow_runner=SubprocessFlowRunner(),
    flow_storage='614add2f-1556-432d-af8d-4821f4cd51bd'
)