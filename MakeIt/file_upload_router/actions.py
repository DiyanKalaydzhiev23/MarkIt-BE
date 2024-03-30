import os
import decouple
import requests

STORAGE_ZONE_NAME = 'markitstorage'
BASE_URL = "storage.bunnycdn.com"


def upload_file_to_bucket(file_data, filename, extension, username):
    url = f"https://{BASE_URL}/{STORAGE_ZONE_NAME}/{username}/{filename}.{extension}"

    headers = {
        "AccessKey": os.getenv('BUNNY_NET_ACCESS_KEY', decouple.config('BUNNY_NET_ACCESS_KEY')),
        "Content-Type": "application/octet-stream",
        "accept": "application/json"
    }

    response = requests.put(url, headers=headers, data=file_data)

    return response


def download_file_from_bucket(filename, extension, username):
    url = f"https://{BASE_URL}/{STORAGE_ZONE_NAME}/{username}/{filename}.{extension}"

    headers = {
        "accept": "*/*",
        "AccessKey": os.getenv('BUNNY_NET_ACCESS_KEY', decouple.config('BUNNY_NET_ACCESS_KEY')),
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_content = response.content
        return file_content
    else:
        print(f"Failed to download file: {response.status_code}")
        return None
