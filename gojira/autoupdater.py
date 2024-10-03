import os
import requests
import shutil
import sys
import tempfile

GITHUB_REPO = "andydobrucki/gojira"  # Replace with your GitHub repository
VERSION_FILE = "version.txt"

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as file:
            return file.read().strip()
    return "0.0"  # Default version if no version file exists

def set_current_version(version):
    with open(VERSION_FILE, 'w') as file:
        file.write(version)

def check_for_update():
    current_version = get_current_version()
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    latest_release = response.json()
    latest_version = latest_release["tag_name"]

    if latest_version > current_version:
        print(f"New version {latest_version} available. Updating...")
        with tempfile.TemporaryDirectory() as tmpdirname:
            if not latest_release["assets"]:
                print("No assets found for the latest release. Downloading source archive instead.")
                download_url = latest_release["zipball_url"]
                download_file(download_url, os.path.join(tmpdirname, "app.zip"))
                shutil.unpack_archive(os.path.join(tmpdirname, "app.zip"), tmpdirname)
            else:
                asset = latest_release["assets"][0]
                download_url = asset["browser_download_url"]
                download_file(download_url, os.path.join(tmpdirname, "app.py"))
            set_current_version(latest_version)
            print("Update complete. Restarting the application.")
            restart_application()

def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

def restart_application():
    python = sys.executable
    os.execv(python, [python] + sys.argv)

if __name__ == "__main__":
    check_for_update()