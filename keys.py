import json
import os
import requests


def get_cognito_public_keys():
    region = "eu-central-1"      #os.environ["AWS_REGION"]
    pool_id = "eu-central-1_SJQdxqfBU" #os.environ["AWS_COGNITO_USER_POOL_ID"]
    url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"

    resp = requests.get(url)
    return json.dumps(json.loads(resp.text)["keys"][1])