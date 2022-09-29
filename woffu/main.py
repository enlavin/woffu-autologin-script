import getpass
import json
import sys
from operator import itemgetter
import os.path
from pathlib import Path
from .woffu import Woffu

CREDENTIALS_FILENAME = '.woffu-autologin-script.json'
LEGACY_CREDENTIALS_FILENAME = 'data.json'

def load_credentials():
    credential_paths = default_credentials_paths()
    for credentials_file in credential_paths:
        if not os.path.exists(credentials_file):
            continue

        try:
            print(f'Using credentials from {credentials_file}')
            with open(credentials_file, "r") as json_data:
                login_info = json.load(json_data)
                username, password = itemgetter(
                    "username",
                    "password",
                )(login_info)

            return True, username, password

        except (OSError, IOError, json.JSONDecodeError):
            pass

    # Ask for user input if there are no credential files created
    username = input("Enter your Woffu username:\n")
    password = getpass.getpass("Enter your password:\n")

    return False, username, password


def default_credentials_paths():
    credential_files = [CREDENTIALS_FILENAME, LEGACY_CREDENTIALS_FILENAME]
    credential_folders = [Path.home(), '.']
    credential_paths = [os.path.join(d, f) for f in credential_files for d in credential_folders]
    return credential_paths


def is_dry_run():
    dry_run_flag = os.environ.get('WOFFU_DRY_RUN', '')
    return dry_run_flag.lower() in ['1', 'yes', 'true']


def run():
    print("Woffu Autologin Script\n")

    has_saved_credentials, username, password = load_credentials()

    woffunator = Woffu(username, password)
    if woffunator.is_working_day_for_me():
        try:
            if (not is_dry_run()):
                woffunator.sign_in()
            else:
                print('Dry-run enabled, no sign-in.')

            print('Success!')
        except Exception as e:
            print(f'Something went wrong when trying to log you in/out: {e.message}')
            sys.exit(1)
    else:
        print('Not a working day. Enjoy!')

    if (not has_saved_credentials):
        credentials_path = default_credentials_paths()[0]
        print(f'Saving credentials to file {credentials_path}')
        woffunator.save_data(credentials_path)
