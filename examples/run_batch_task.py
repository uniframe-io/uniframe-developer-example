import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
import time
from io import StringIO
import pandas as pd
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login
from examples.create_batch_task import get_batch_task_id


def run_batch_task(access_token: str, task_id: int) -> str:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_id: batch task id
    :return: message of running batch task
    """
    url = f"{HOST_URL}/api/v1/tasks/nm/{task_id}/start"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_task_status(access_token: str, task_id: int) -> str:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_id: task id get from `create_batch_task`
    :return: task status
    """

    url = f"{HOST_URL}/api/v1/tasks/nm/{task_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res_dict = response.json()
    return res_dict['ext_info']['nm_status']


def print_batch_task_result(task_id: int):
    """
    :param task_id: batch task id
    :return:
    """
    url = f"{HOST_URL}/api/v1/tasks/nm/{task_id}/download-batch-result"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    s3_url = response.text

    response = requests.request("GET", s3_url.strip('"'))
    data = StringIO(response.text)
    df = pd.read_csv(data, sep=",")
    print(df)


if __name__ == "__main__":
    # step 1
    # login with username and password
    login_res = login(USERNAME, PASSWORD)
    print("Login with username and password in .env file successful")

    access_token = login_res['access_token']

    # step 2
    # get real time task id just created in `create_rt_task`
    task_id = get_batch_task_id(access_token, "my batch task")

    # step 3
    # run batch task
    run_res = run_batch_task(access_token, task_id)
    print(run_res)

    # step 4
    # make sure task is terminated
    task_status: str = 'init'
    while task_status != 'complete':
        time.sleep(1)
        task_status = get_task_status(access_token, task_id)

    print("task launch successfully")

    # step 4
    # get result
    print_batch_task_result(task_id)




