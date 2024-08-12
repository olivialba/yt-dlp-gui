import requests, zipfile, json, os, io

DATA_URL = 'https://raw.githubusercontent.com/olivialba/yt-dlp-gui/main/updater/data.json'
DATA_JSON = 'updater/data.json'
S = "   "
FOLDER_PREFIX = ''
TEXT_FILE_EXTENSIONS = (
    '.py',  # Python scripts
    '.txt',  # Plain text files
    '.md',  # Markdown files
    '.json',  # JSON data files
    '.xml',  # XML files
    '.html',  # HTML files
    '.htm',  # HTML files
    '.css',  # Cascading Style Sheets
    '.js',  # JavaScript files
    '.csv',  # Comma-separated values
    '.yaml',  # YAML files
    '.yml',  # YAML files
    '.ini',  # Initialization files
    '.cfg',  # Configuration files
    '.log',  # Log files
    '.sh',  # Shell scripts
    '.bat',  # Batch files
    '.pl',  # Perl scripts
    '.php',  # PHP scripts
    '.rb',  # Ruby scripts
    '.java',  # Java source files
    '.c',  # C source files
    '.cpp',  # C++ source files
    '.h',  # Header files
    '.hpp',  # C++ header files
    '.sql',  # SQL files
    '.rtf',  # Rich Text Format files
    '.tex',  # LaTeX files
    '.r',  # R script files
    '.go',  # Go language source files
    '.rs',  # Rust source files
    '.swift',  # Swift source files
    '.ts',  # TypeScript files
    '.vue',  # Vue.js single-file components
    '.toml',  # TOML configuration files
    '.env',  # Environment configuration files
    '.dart',  # Dart source files
    '.groovy',  # Groovy scripts
    '.ps1',  # PowerShell scripts
    '.xslt',  # XSLT stylesheets
    '.conf',  # Configuration files
    '.tsv',  # Tab-separated values
    '.properties',  # Java properties files
    '.gradle',  # Gradle build scripts
)


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
        check = FOLDER_PREFIX + folder
        if os.path.exists(check) and os.path.isdir(check):
            print(f"{S}  '{check}' exists.")
        else:
            print(f"{S}ERROR: '{check}' does NOT exists..")
            count += 1
    for file in files:
        check = FOLDER_PREFIX + file
        if os.path.exists(check) and os.path.isfile(check):
            print(f"{S}  '{check}' exists.")
        else:
            print(f"{S}ERROR: '{check}' does NOT exists..")
            count +=1
    print(f"\n* Missing {count} files and folders!")


    
def normal_update(new_data, old_data):
    n_v = new_data['version']
    o_v = old_data['version']
    print(f'{o_v} -> {n_v}')
    check_files(new_data)

    to_folders = new_data['to_update']['folders']
    to_files = new_data['to_update']['files']
    print()
    try:
        for folder in to_folders:
            check = FOLDER_PREFIX + folder
            if not os.path.exists(check) or not os.path.isdir(check):
                print(f"Creating folder '{check}'")
                os.makedirs(check)
        for file in to_files:
            check = FOLDER_PREFIX + file
            print(f"Updating file '{check}'")
            url = new_data['github']['raw_link'] + file

            response = requests.get(url)
            if response.status_code == 200:
                if file.endswith(TEXT_FILE_EXTENSIONS):
                    content = response.text
                    with open(check, 'w', encoding='utf-8') as f:
                        f.write(content)
                else:
                    content = response.content
                    with open(check, 'wb') as f:
                        f.write(content)
            else:
                print(f"Can't get request for updating {check}. Status code: {response.status_code}")
                raise Exception
    except Exception as e:
        print(e)
        print('CRITICAL ERROR while updating.. Stopping..')
        return None
    return True


def UPDATER_START():
    status = None

    new_data = get_data(DATA_URL)
    if new_data is None:
        return None
    
    with open(DATA_JSON, 'r') as file:
        old_data = json.load(file)

    new_version = new_data['version']
    old_version = old_data['version']

    if old_version == new_version:
        print("No new update found..")
        return False
    
    elif (old_version + 0.1) == new_version:
        print('Update starting...')
        status = normal_update(new_data, old_data)
    elif (old_version + 0.1) < new_version:
        print('Program is two versions old. Downloading latest files...')
    else:
        print('Error found with version. Downloading latest files...')
    
    if status is not False and status is not None:
        print("Updating successful!")
        with open(DATA_JSON, 'w') as file:
            json.dump(new_data, file, indent=4)
        return True
    else:
        return None
    
