import sys
import os
import random

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
import json
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login
from examples.create_dataset import upload_media, create_dataset


def create_rt_task(access_token: str, dataset_id: int, rt_task_name: str) -> dict:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param dataset_id: dataset id get from `create_dataset`
    :param rt_task_name: name of realtime task that you want to set
    :return: dict response of create real time task
    """
    url = f"{HOST_URL}/api/v1/tasks/nm"

    payload = json.dumps({
        "name": rt_task_name,
        "description": "rt task description",
        "is_public": False,
        "type": "NAME_MATCHING_REALTIME",
        "ext_info": {
            "nm_status": "init",
            "gt_dataset_config": {
                "dataset_id": dataset_id,
                "search_key": "Company name"
            },
            "computation_resource": {
                "computation_type": "multi-thread",
                "computation_config": {
                    "resource_tshirt_size": "Small"
                }
            },
            "running_parameter": {
                "TTL_enable": True,
                "TTL": "P0DT0H30M0S"
            },
            "search_option": {
                "top_n": 1,
                "threshold": 0.5,
                "selected_cols": []
            },
            "algorithm_option": {
                "type": "VECTOR_BASED",
                "value": {
                    "preprocessing_option": {
                        "case_sensitive": False,
                        "company_legal_form_processing": True,
                        "initial_abbr_processing": False,
                        "punctuation_removal": True,
                        "accented_char_normalize": False,
                        "shorthands_format_processing": False
                    },
                    "tokenizer_option": "WORD",
                    "cos_match_type": "EXACT",
                    "postprocessing_option": {
                        "placeholder": "placeholder"
                    }
                }
            },
            "abcxyz_privacy": {
                "data_retention_time": "P30DT0H0M0S",
                "log_retention_time": "P30DT0H0M0S"
            },
            "abcxyz_security": {
                "encryption": "sse-s3"
            }
        }
    })

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def get_task_status(access_token: str, task_id: int) -> str:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_id: task id get from `create_rt_task`
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


def get_rt_task_id(access_token: str, task_name: str) -> int:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_name: task name you created by `create_rt_task`
    :return: real time task id
    """
    url = f"{HOST_URL}/api/v1/tasks/nm?nm_type=NAME_MATCHING_REALTIME"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    dict_res = response.json()
    for t in dict_res:
        if t['name'] == task_name:
            return t['id']


if __name__ == "__main__":
    # step 1
    # login with username and password
    login_res = login(USERNAME, PASSWORD)
    print("Login with username and password in .env file successful")

    # steop 2
    # upload file of dataset
    access_token = login_res['access_token']
    upload_media_res = upload_media(access_token, "demo-gt")
    print(upload_media_res)

    # step 3
    # create dataset
    media_id = upload_media_res["id"]
    create_dateset_res = create_dataset(access_token, media_id, f"my gt dataset")
    print(create_dateset_res)

    # step 4
    # create real time task
    dataset_id = create_dateset_res["id"]
    create_rt_task_res = create_rt_task(access_token, dataset_id, f"my rt task")
    print(create_rt_task_res)


