import requests
from pathlib import Path
import platform
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
from zipfile import ZipFile
from io import BytesIO
import os


def download_and_extract_zip(url, target_path):
    response = requests.get(url, stream=True, verify=False)
    
    if response.status_code == 200:
        data = BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            data.write(chunk)

        with ZipFile(data, 'r') as zip_ref:
            exe_files = [file for file in zip_ref.namelist() if os.path.splitext(file)[1] == '.exe']
            if exe_files:
                arch = exe_files[0]
                name = os.path.basename(arch)
                with zip_ref.open(arch) as myfile:
                    with open(os.path.join(target_path, name), 'wb') as file:
                        file.write(myfile.read())
    else:
        print(f"Error: HTTP status code {response.status_code}. Unable to download the file.")

def main():
    try:
        home = Path.home()
        dir = home / '.azcp'
        dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir}")

        # config_template_base_url = "https://github.com/yusuf-jkhan1/azpype/blob/main/setup/assets/config_templates"
        # config_template_files = ["copy_config.yaml"]  # Add more when/if needed

        # for config_file in config_template_files:
        #     download_file(f"{config_template_base_url}/{config_file}?raw=true", dir / config_file)
        #     print(f"Downloaded config file: {config_file}")

        # binary_base_url = "https://github.com/yusuf-jkhan1/azpype/blob/main/setup/assets/bin"
        binary_name = None

        if platform.system() == 'Darwin':
            binary_name = 'https://aka.ms/downloadazcopy-v10-mac'
        elif platform.system() == 'Windows':
            binary_name = 'https://aka.ms/downloadazcopy-v10-windows'
        elif platform.system() == 'Linux':
            if platform.machine() == 'x86_64':
                binary_name = 'https://aka.ms/downloadazcopy-v10-linux'
            elif platform.machine() == 'aarch64':
                binary_name = 'https://aka.ms/downloadazcopy-v10-linux-arm64'


        if binary_name:
            download_and_extract_zip(f'{binary_name}', dir)
            print(f"Downloaded url: {binary_name}, system: {platform.system()}, machine: {platform.machine() }")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()