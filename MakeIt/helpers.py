import json
import os
import decouple
import requests


def upload_file_to_bucket(file_data, filename, extension, username):
    region = ''
    storage_zone_name = 'markitstorage'

    base_url = "storage.bunnycdn.com"
    if region:
        base_url = f"{region}.{base_url}"

    url = f"https://{base_url}/{storage_zone_name}/{username}/{filename}.{extension}"

    headers = {
        "AccessKey": os.getenv('BUNNY_NET_ACCESS_KEY', decouple.config('BUNNY_NET_ACCESS_KEY')),
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    response = requests.put(url, headers=headers, data=file_data)

    return response


def serialize_dump_json(data):
    result = []

    for record in data:
        result.append(json.dumps(record))

    return result


def serialize_load_json(data):
    result = []

    for record in data:
        result.append(json.loads(record))

    return result