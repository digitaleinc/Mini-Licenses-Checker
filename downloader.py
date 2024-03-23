import requests
from pathlib import Path


def download_file_from_api(api_url, project, licence_k, file_name, downloaded_filename):
    try:
        response = requests.get(api_url,
                                params={"project_name": project,
                                        "file_name": file_name,
                                        "license_key": licence_k})

        if response.status_code == 200:
            script_folder = Path(__file__).parent
            file_path = script_folder / f'{downloaded_filename}'

            with open(file_path, 'wb') as file:
                file.write(response.content)

            print(f"File '{file_name}' downloaded and saved successfully.")
        elif response.status_code == 404:
            print(f"Error - NOT FOUND")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Failed to download file. Please, check your connection")


if __name__ == "__main__":
    updater_url = 'http://127.0.0.1:6061/get_update'
    file_name_to_download = 'test.txt'
    set_downloaded_filename = 'testing.txt'

    project_name = 'test'

    licence_key = '10f3a058-ba2c-40fd-be4f-14920b87af24'

    download_file_from_api(updater_url, project_name, licence_key, file_name_to_download, set_downloaded_filename)
