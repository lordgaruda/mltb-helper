from __future__ import print_function

import argparse
import glob
import googleapiclient.discovery
import json
import os
import pickle
import progress.bar
import sys
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

stt = time.time()

parse = argparse.ArgumentParser(
    description="A tool to remove service accounts from a shared drive."
)
parse.add_argument(
    "--path",
    "-p",
    default="accounts",
    help="Specify an alternative path to the service accounts folder.",
)
parse.add_argument(
    "--credentials",
    "-c",
    default="./credentials.json",
    help="Specify the relative path for the credentials file.",
)
parse.add_argument(
    "--yes", "-y", default=False, action="store_true", help="Skips the sanity prompt."
)
parsereq = parse.add_argument_group("required arguments")
parsereq.add_argument(
    "--drive-id", "-d", help="The ID of the Shared Drive.", required=True
)

args = parse.parse_args()
acc_dir = args.path
did = args.drive_id
credentials = glob.glob(args.credentials)

try:
    open(credentials[0], "r")
    print(">> Found credentials.")
except IndexError:
    print(">> No credentials found.")
    sys.exit(0)

if not args.yes:
    input(
        ">> Make sure the **Google account** that has generated credentials.json\n   is added into your Team Drive "
        "(shared drive) as Manager\n>> (Press any key to continue)"
    )

creds = None
if os.path.exists("token_sa.pickle"):
    with open("token_sa.pickle", "rb") as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials[0],
            scopes=[
                "https://www.googleapis.com/auth/drive",
            ],
        )
        creds = flow.run_console()
    with open("token_sa.pickle", "wb") as token:
        pickle.dump(creds, token)

drive = googleapiclient.discovery.build("drive", "v3", credentials=creds)

aa = glob.glob(f"{acc_dir}/*.json")
pbar = progress.bar.Bar("Readying accounts for removal", max=len(aa))
for i in aa:
    ce = json.loads(open(i, "r").read())["client_email"]
    try:
        permissions = drive.permissions().list(
            fileId=did, supportsAllDrives=True, fields="permissions(id,emailAddress)"
        ).execute()
        for perm in permissions.get("permissions", []):
            if perm["emailAddress"] == ce:
                drive.permissions().delete(
                    fileId=did, permissionId=perm["id"], supportsAllDrives=True
                ).execute()
                break
    except Exception as e:
        print(f"Error removing {ce}: {e}")
    pbar.next()
pbar.finish()

print("Removal complete.")
hours, rem = divmod((time.time() - stt), 3600)
minutes, sec = divmod(rem, 60)
print("Elapsed Time:\n{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), sec))
