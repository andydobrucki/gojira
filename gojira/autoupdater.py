import requests
import shutil
import sys

GITHUB_REPO = "username/repo"  # Replace with your GitHub repository
CURRENT_VERSION = "0.1"  # Replace with your current version

def check_for_update():
    url = f"https://api.github.com/repos/andydobrucki/gojira/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    latest_release = response.json()
    latest_version = latest_release["tag_name"]

    if latest_version > CURRENT_VERSION:
        print(f"New version {latest_version} available. Updating...")
        asset = latest_release["assets"][0]
        download_url = asset["browser_download_url"]
        download_file(download_url, "app.py")
        print("Update complete. Please restart the application.")
        sys.exit()

def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

if __name__ == "__main__":
    check_for_update()