import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import time
import requests
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login
from examples.create_rt_task import get_task_status, get_rt_task_id


def launch_rt_task(access_token: str, task_id: int) -> str:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_id: real time task id
    :return: launch message
    """
    url = f"{HOST_URL}/api/v1/tasks/nm/{task_id}/start"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


if __name__ == "__main__":
    # step 1
    # login with username and password
    login_res = login(USERNAME, PASSWORD)
    print("Login with username and password in .env file successful")

    access_token = login_res['access_token']
    # step 2
    # get real time task id just created in `create_rt_task`
    rt_id = get_rt_task_id(access_token, "my rt task")

    # step 3
    # launch task
    launch_res = launch_rt_task(access_token, rt_id)
    print(launch_res)

    # step 4
    # make sure task is ready
    task_status: str = 'init'
    while task_status != 'ready':
        time.sleep(1)
        task_status = get_task_status(access_token, rt_id)

    print("task launch successfully")





