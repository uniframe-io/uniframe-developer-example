import sys
import os
from typing import Any

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login
from examples.create_rt_task import get_rt_task_id
from examples.create_batch_task import get_batch_task_id
from examples.create_dataset import get_dataset_id


def delete_dataset(access_token: str, dataset_id: int) -> Any:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param dataset_id: dataset id get from `get_dataset_id`
    :return:
    """
    url = f"{HOST_URL}/api/v1/datasets/{dataset_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text)


def delete_task(access_token: str, task_id: int) -> Any:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_id: dataset id get from `get_rt_task_id` or `get_batch_task_id`
    :return:
    """
    url = f"{HOST_URL}/api/v1/tasks/{task_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text)


if __name__ == "__main__":
    # step 1
    # login with username and password
    login_res = login(USERNAME, PASSWORD)
    print("Login with username and password in .env file successful")

    # steop 2
    # upload file of dataset
    access_token = login_res['access_token']

    # step 3
    # delete tasks created in examples
    rt_task_id = get_rt_task_id(access_token, "my rt task")
    if rt_task_id:
        delete_task(access_token, rt_task_id)

    batch_task_id = get_batch_task_id(access_token, "my batch task")
    if batch_task_id:
        delete_task(access_token, batch_task_id)

    # step 4
    # delete datasets created in examples

    for dataset_name in ["my gt dataset for batch task", "my nm dataset for batch task", "my gt dataset", "gt dataset"]:
        dataset_id = get_dataset_id(access_token, dataset_name)
        if dataset_id:
            delete_dataset(access_token, dataset_id)

