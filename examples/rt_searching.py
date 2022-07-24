import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import json
import requests
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login
from examples.create_rt_task import get_task_id


def rt_task_search(access_token: str, task_id: int) -> dict:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param task_id: real time task id
    :return: search result
    """
    url = f"{HOST_URL}/api/v1/tasks/nm/{task_id}/match"

    payload = json.dumps({
      "query_keys": [
        "Sun"
      ],
      "search_option": {
        "top_n": 2,
        "threshold": 0.7,
        "selected_cols": [
          "Company name",
          "Company id"
        ]
      }
    })

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


if __name__ == "__main__":
    # step 1
    # login with username and password
    login_res = login(USERNAME, PASSWORD)
    print("Login with username and password in .env file successful")

    access_token = login_res['access_token']
    # step 2
    # get real time task id just created in `create_rt_task`
    rt_id = get_task_id(access_token, "my rt task")

    # step 3
    # search
    rt_search_res = rt_task_search(access_token, rt_id)
    print(rt_search_res)

