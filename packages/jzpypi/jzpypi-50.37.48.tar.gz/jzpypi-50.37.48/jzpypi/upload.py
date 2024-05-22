import os
import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

def upload_package(username, password, skip_existing, repository_url, dist_files):
    for filepath in dist_files:
        filename = os.path.basename(filepath)

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
                elif response.status_code == 409 and skip_existing:
                    print(f"File {filename} already exists. Skipping due to --skip-existing.")
                else:
                    print(f"Failed to upload {filename}")
                    print(f"Status code: {response.status_code}")
                    print(f"Response: {response.text}")

def main():
    username = '__token__'
    password = input("Enter your PyPI API token: ")
    dist_files = input("Enter the paths of distribution files to upload (separated by spaces): ").split()
    skip_existing = True  # You can change this if you want to skip existing files or not
    repository_url = 'https://upload.pypi.org/legacy/'

    upload_package(username, password, skip_existing, repository_url, dist_files)

if __name__ == "__main__":
    main()
