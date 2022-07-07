from asyncio import tasks
from dataclasses import field
import os
from dotenv import load_dotenv
import requests
import pandas as pd
from prefect import flow, task
import time
import random

@task(name="make-auth-header")
def make_authentication_header(TWITTER_BEARER_TOKEN):

    # TWITTER_BEARER_TOKEN = None
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    print(headers)
    assert len(str(headers)) > 56

    return headers

@task(name='Sleeping Task')
def sleeping_flow():
    time.sleep(3)
    outcome = random.choice(['Pass', 'Pass', 'Pass'])
    print("Random Outcome")
    print(outcome)
    assert outcome == 'Pass'
    return "Hi!"


@task(name="make-user-param-string")
def make_user_param_string(users, hi):

    print(hi)
    if type(users) != str:
        users_url_string = ','.join(users)
        username_param = f'by?usernames={users_url_string}' 
        return username_param
    else:
        username_param = f'by?usernames={users}'
        return username_param

@task(name="make-field-param-string")
def make_fields_param_string(fields):
    
    if type(fields) != str:
        fields_url_string = ','.join(fields)
        fields_param = f'&user.fields={fields_url_string}'
    else:
        fields_param = f'&user.fields={fields}'
        return fields_param

@task(name="call-api")
def make_api_call(headers, username_param, fields_param='&user.fields=public_metrics'):
    base_url = 'https://api.twitter.com/2/users/'
    print(base_url + username_param + fields_param)
    response = requests.request(
        "GET", 
        base_url + username_param + fields_param, 
        headers=headers
        )
    try:
        assert str(response.status_code).startswith('2')
        print(response.json())
    except:
        print(response.text)

    assert str(response.status_code).startswith('2')
    return response

from prefect.task_runners import SequentialTaskRunner

@flow(name="Get User Data from Twitter API",
      version=os.getenv("GIT_COMMIT_SHA"))
def data_output(TWITTER_BEARER_TOKEN, users, fields):

    headers = make_authentication_header(TWITTER_BEARER_TOKEN)
    print("HERE")
    print(headers)
    hi = sleeping_flow()
    user_string = make_user_param_string(users, hi)
    field_string = make_fields_param_string(fields)
    response = make_api_call(headers, user_string, field_string)
    return response

