import getpass
import json
import sys
from operator import itemgetter
import os.path
from .woffu import Woffu

def run():
    print("Woffu Autologin Script\n")
    saved_credentials = os.path.exists("./data.json")
    if (saved_credentials):
        with open("./data.json", "r") as json_data:
            login_info = json.load(json_data)
            domain, username, password, user_id, company_id = itemgetter(
                "domain",
                "username",
                "password",
                "user_id",
                "company_id"
            )(login_info)
    else:
        username = input("Enter your Woffu username:\n")
        password = getpass.getpass("Enter your password:\n")

    client = Woffu(username, password)
    if client.is_working_day_for_me():
        try:
            client.sign_in()
            print('Success!')
        except Exception as e:
            print("Something went wrong when trying to log you in/out: {}".format(e.message))
            sys.exit(1)
    else:
        print("Not a working day. Enjoy!")

    if (not saved_credentials):
        client.save_data()
