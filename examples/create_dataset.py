import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
import pathlib
import json
from examples.config import HOST_URL, USERNAME, PASSWORD
from examples.login_get_bearer_token import login


def upload_media(access_token: str, file_name: str) -> dict:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param file_name: file name of media
    :return: dict response of uploading media
    """
    url = f"{HOST_URL}/api/v1/medias/upload"
    cwd = pathlib.Path.cwd()
    files = [
        ('file', ('demo-gt.csv', open(f'{cwd}/assets/data/{file_name}.csv', 'rb'), 'text/csv'))
    ]
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data={}, files=files)
    upload_res = response.json()
    return upload_res


def create_dataset(access_token: str, media_id: int, dataset_name: str) -> dict:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param media_id: media id get from `upload_media`
    :param dataset_name: the name of dataset you want to set
    :return: dict response of creating dataset
    """
    url = f"{HOST_URL}/api/v1/datasets"
    payload = json.dumps({
        "name": dataset_name,
        "description": "my dataset description",
        "media_id": media_id
    })
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    create_dataset_res = response.json()
    return create_dataset_res


def get_dataset_id(access_token: str, dataset_name: str) -> int:
    """
    :param access_token: access token get from `login_get_bearer_token`
    :param dataset_name: the name of dataset you just create
    :return: dataset id
    """
    url = f"{HOST_URL}/api/v1/datasets"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    dict_res = response.json()
    for d in dict_res:
        if d['name'] == dataset_name:
            return d['id']


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
    create_dateset_res = create_dataset(access_token, media_id, f"gt dataset")
    print(create_dateset_res)
