from asyncio import tasks
from dataclasses import field
import os
from dotenv import load_dotenv
import requests
import pandas as pd
from prefect import flow, task

@task(name="make-auth-header")
def make_authentication_header(BEARER_TOKEN):
    load_dotenv()
    TWITTER_BEARER_TOKEN=os.getenv(BEARER_TOKEN)

    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}

    return headers

@task(name="make-user-param-string")
def make_user_param_string(users):

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
    response = requests.request(
        "GET", 
        base_url + username_param + fields_param, 
        headers=headers
        )

    return response


@flow(name="Get User Data from Twitter API",
      version=os.getenv("GIT_COMMIT_SHA"))
def data_output(BEARER_TOKEN, users, fields):

    headers = make_authentication_header(BEARER_TOKEN)
    user_string = make_user_param_string(users)
    field_string = make_fields_param_string(fields)
    response = make_api_call(headers, user_string, field_string)
    return response.result().json()

if __name__ == '__main__':

    # Input data
    users = [
        'apacheairflow', 
        'astronomerio'
        ]
    fields = 'public_metrics'

    r = data_output(BEARER_TOKEN='TWITTER_BEARER_TOKEN', users=users, fields=fields)

    print(r.result())
    print('Done!')


