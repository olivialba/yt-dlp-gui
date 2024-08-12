import requests, zipfile, json, os, io

DATA = 'https://raw.githubusercontent.com/olivialba/yt-dlp-gui/main/updater/data.json'
PARENT_FOLDER = '../'

def get_data(url):
    try:
        req = requests.get(url)
        if req.status_code != 200:
            print(f"Error. Can't reach server. Request status: {req.status_code}")
            return None
        else:
            return req.json()
    except requests.exceptions.JSONDecodeError:
        print("Error. Couldn't convert request's text to json.")
        return None
    
def check_files(data):
    count = 0
    folders = data['content']['folders']
    files = data['content']['files']
    print("\nChecking existing files and folders:")
    for folder in folders:
        check = PARENT_FOLDER + folder
        if os.path.exists(check) and os.path.isdir(check):
            print(f"{check} exists..")
        else:
            print(f"ERROR: {check} does NOT exists..")
            count += 1
    for file in files:
        check = PARENT_FOLDER + file
        if os.path.exists(check) and os.path.isfile(check):
            print(f"{check} exists..")
        else:
            print(f"ERROR: {check} does NOT exists..")
            count +=1
    print(f"* Missing {count} files and folders.")


    
def normal_update(new_data, old_data):
    check_files(new_data)
    to_folders = new_data['to_update']['folders']
    to_files = new_data['to_update']['files']
    print()
    try:
        for folder in to_folders:
            check = PARENT_FOLDER + folder
            if not os.path.exists(check) or not os.path.isdir(check):
                print(f"Creating folder {check}.")
                os.makedirs(check)
        for file in to_files:
            check = PARENT_FOLDER + file
            if os.path.exists(check) and os.path.isfile(check):
                print(f"Updating file {check}.")
                url = new_data['github']['raw_link'] + file

                response = requests.get(url)
                if response.status_code == 200:
                    content = response.text
                    with open(check, 'w') as f:
                        f.write(content)
                else:
                    print(f"Can't get request for updating {check}. Status code: {response.status_code}")
                    raise Exception
    except:
        print('CRITICAL ERROR while updating.. Stopping..')
        return None
    return True


def UPDATER_START():
    status = None

    new_data = get_data(DATA)
    if new_data is None:
        return None
    
    with open("data.json", 'r') as file:
        old_data = json.load(file)

    new_version = new_data['version']
    old_version = old_data['version']

    if old_version == new_version:
        print("No new update found..")
        return None
    
    elif (old_version + 0.1) == new_version:
        print('Update starting...')
        status = normal_update(new_data, old_data)
    elif (old_version + 0.1) < new_version:
        print('Program is two versions old. Downloading latest files...')
    else:
        print('Error found with version. Downloading latest files...')
    
    if status is not False and status is not None:
        print("Updating successful!")
    
