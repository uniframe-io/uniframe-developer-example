import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from examples.config import HOST_URL, USERNAME, PASSWORD


def login(username: str, password: str) -> dict:
    """
    :param username: email that used for signup
    :param password: password
    :return: dict response of login
    """
    url = f"{HOST_URL}/api/v1/login"

    payload = {
        'username': username,
        'password': password,
    }
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()


if __name__ == "__main__":
    # step 1
    # login with email and password
    login_res = login(USERNAME, PASSWORD)
    print("Login with username and password in .env file successful")
