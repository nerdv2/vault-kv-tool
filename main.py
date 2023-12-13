#!/usr/bin/python3
import argparse
import requests
import json
import os
from pathlib import Path

# parse arguments
parser = argparse.ArgumentParser(description='Retrieve KV data from Vault.')
parser.add_argument('domain', metavar='domain', type=str, help='target domain')
parser.add_argument('--token', metavar='token', type=str,
                    help='define token value (default: reading env value of VAULT_TOKEN)')
parser.add_argument('--vault', metavar='vault', type=str,
                    help='define vault host value (default: reading env value of VAULT_URL)')
                    
args = parser.parse_args()

token = os.getenv("VAULT_TOKEN")
url = os.getenv("VAULT_URL")
vault_base_path = 'server_environment'

if not token:
    if args.token:
        token = args.token
    else:
        print("Unable to read token from VAULT_TOKEN environment variable or arguments.")
        exit()

if not url:
    if args.vault:
        url = args.vault
    else:
        print("Unable to read vault host from VAULT_URL environment variable or arguments.")
        exit()

print(args.domain)
if args.domain:
    headers = {'X-Vault-Request': "true", "X-Vault-Token": token}

    r = requests.get(url + "/v1/server_environment/data/" + args.domain, headers=headers)

    try:
        result = json.loads(r.text)['data']['data']

        check_file = Path(args.domain)
        if check_file.is_file():
            check_file.unlink()

        for key in result:
            value = result[key]
            print("Writing ({}) = ({})".format(key, value))

            with open(args.domain, "a") as final_file:
                final_file.write(key + "=" + value +"\n")
    except:
        print("Domain not found or invalid token.")