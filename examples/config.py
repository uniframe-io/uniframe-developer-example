import os
from dotenv import load_dotenv

load_dotenv()

HOST_URL = "https://api.uniframe.io"
USERNAME = os.getenv('USERNAME')
if USERNAME is None:
    raise ValueError("Please add env variable USERNAME is .env file")
PASSWORD = os.getenv('PASSWORD')
if PASSWORD is None:
    raise ValueError("Please add env variable PASSWORD is .env file")
