#!/usr/bin/env python3

import os
import json


irc_credentials_path = os.path.expanduser("~/.config/anna/irc_credentials.json")

def get_irc_credentials():
    return get_irc_credentials_path(irc_credentials_path)

def get_irc_credentials_path(path):
    with open(path, 'r') as f:
        j = json.load(f)
    return j


if __name__ == '__main__':
    creds = get_irc_credentials_path("irc_credentials.json.template")
    print(creds)