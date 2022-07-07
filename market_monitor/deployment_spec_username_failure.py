
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner
from dotenv import load_dotenv
import os

load_dotenv()
TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN")

DeploymentSpec(
    name="twitter-user-query-flow-FAILURE-USERNAME",
    flow_location="./twitter_user_query_flow.py",
    flow_name="Get User Data from Twitter API",
    parameters={
        'TWITTER_BEARER_TOKEN': os.environ['TWITTER_BEARER_TOKEN'],
        'users':[
            'https://stackoverflow.com/questions/25016301',
            'https://api.github.com/repositories?since=+str'
            ],
            'fields': 'public_metrics'
        },
    tags=['Twitter_API'],
    flow_runner=SubprocessFlowRunner(env={"TWITTER_BEARER_TOKEN": TWITTER_BEARER_TOKEN}),
    flow_storage='614add2f-1556-432d-af8d-4821f4cd51bd'
)