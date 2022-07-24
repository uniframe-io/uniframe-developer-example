import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
import json
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login
from examples.create_dataset import upload_media, create_dataset


def create_batch_task(access_token: str, gt_dataset_id: int, nm_dataset_id: int, batch_task_name: str) -> dict:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param gt_dataset_id: ground truth dataset id
    :param nm_dataset_id: name matching dataset id
    :param batch_task_name: batch task name you want to set
    :return: dict response of creating batch task
    """
    url = f"{HOST_URL}/api/v1/tasks/nm"

    payload = json.dumps({
        "name": batch_task_name,
        "description": "batch task example",
        "is_public": False,
        "type": "NAME_MATCHING_BATCH",
        "ext_info": {
            "nm_status": "init",
            "gt_dataset_config": {
                "dataset_id": gt_dataset_id,
                "search_key": "Company name"
            },
            "nm_dataset_config": {
                "dataset_id": nm_dataset_id,
                "search_key": "matching name"
            },
            "computation_resource": {
                "computation_type": "multi-thread",
                "computation_config": {
                    "resource_tshirt_size": "Small"
                }
            },
            "running_parameter": {
                "TTL_enable": True,
                "TTL": "P0DT0H15M0S"
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
            "matching_result": None,
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


def get_batch_task_id(access_token: str, task_name: str) -> int:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_name: task name you used in `create_batch_task`
    :return: batch task id
    """
    url = f"{HOST_URL}/api/v1/tasks/nm?nm_type=NAME_MATCHING_BATCH"

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

    access_token = login_res['access_token']
    # step 2
    # upload ground truth data file
    gt_media_res = upload_media(access_token, "demo-gt")
    print(gt_media_res)

    # step 3
    # create groud truth dataset
    gt_media_id = gt_media_res["id"]
    gt_dateset_res = create_dataset(access_token, gt_media_id, "my gt dataset for batch task")
    print(gt_dateset_res)

    gt_dataset_id = gt_dateset_res["id"]
    # step 4
    # upload name matching data file
    nm_media_res = upload_media(access_token, "demo-matching")
    print(nm_media_res)

    nm_media_id = nm_media_res["id"]
    # step 5
    # create name matching dataset
    nm_dateset_res = create_dataset(access_token, nm_media_id, "my nm dataset for batch task")
    print(nm_dateset_res)

    nm_dataset_id = nm_dateset_res["id"]
    # step 6
    # create batch task
    create_rt_task_res = create_batch_task(access_token, gt_dataset_id, nm_dataset_id, "my batch task")
    print(create_rt_task_res)
