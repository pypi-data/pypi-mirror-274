import os
import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

def check_existing_files(username, password, repository_url):
    # Get a list of existing files on PyPI
    response = requests.get(repository_url, auth=HTTPBasicAuth(username, password))
    if response.status_code != 200:
        print(f"Failed to fetch existing files from PyPI. Status code: {response.status_code}")
        return []

    # Extract the filenames from the response
    lines = response.text.split('\n')
    filenames = [line.split('<a href="')[1].split('">')[0] for line in lines if 'class="filename"' in line]
    return filenames

def upload_package(username, password, repository_url, dist_folder):
    # Get a list of existing files on PyPI
    existing_files = check_existing_files(username, password, repository_url)

    # Get a list of files in the specified folder
    dist_files = [os.path.join(dist_folder, filename) for filename in os.listdir(dist_folder)]

    for filepath in dist_files:
        filename = os.path.basename(filepath)

        # Check if the file has already been uploaded
        if filename in existing_files:
            print(f"File {filename} already exists on PyPI. Skipping.")
            continue

        # Check if the file exists before attempting to upload
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        with open(filepath, 'rb') as f:
            file_size = os.path.getsize(filepath)
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=filename) as progress_bar:
                def progress_callback(monitor):
                    progress_bar.update(monitor.bytes_read - progress_bar.n)

                encoder = MultipartEncoder(
                    fields={'content': (filename, f), 'protocol_version': '1'}
                )
                monitor = MultipartEncoderMonitor(encoder, progress_callback)

                print(f"Uploading {filename}...")
                response = requests.post(
                    repository_url,
                    auth=HTTPBasicAuth(username, password),
                    data=monitor,
                    headers={'Content-Type': monitor.content_type}
                )

                if response.status_code == 200:
                    print(f"Successfully uploaded {filename}")
                else:
                    print(f"Failed to upload {filename}")
                    print(f"Status code: {response.status_code}")
                    print(f"Response: {response.text}")

def main():
    username = '__token__'
    password = input("Enter your PyPI API token: ")
    dist_folder = input("Enter the path to the folder containing distribution files: ")
    repository_url = 'https://upload.pypi.org/legacy/'

    upload_package(username, password, repository_url, dist_folder)

if __name__ == "__main__":
    main()
