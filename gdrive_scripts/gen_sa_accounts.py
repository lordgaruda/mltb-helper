import errno
import os
import pickle
import sys
# ...existing code...
from googleapiclient.errors import HttpError
from json import loads
from random import choice
from time import sleep

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/iam",
]
# ...existing code...
def _create_accounts(service, project, count):
    batch = service.new_batch_http_request(callback=_def_batch_resp)
# ...existing code...
def _create_remaining_accounts(iam, project):
    print(f"Creating accounts in {project}")
# ...existing code...
def _generate_id(prefix="saf-"):
    chars = "-abcdefghijklmnopqrstuvwxyz1234567890"
# ...existing code...
def _get_projects(service):
    return [i["projectId"] for i in service.projects().list().execute()["projects"]]
# ...existing code...
def _def_batch_resp(id, resp, exception):
    if exception is not None:
# ...existing code...
def _pc_resp(id, resp, exception):
    global project_create_ops
# ...existing code...
def _create_projects(cloud, count):
    global project_create_ops
# ...existing code...
def _enable_services(service, projects, ste):
    batch = service.new_batch_http_request(callback=_def_batch_resp)
# ...existing code...
def _list_sas(iam, project):
    resp = (
        iam.projects()
        .serviceAccounts()
        .list(name=f"projects/{project}", pageSize=100)
        .execute()
    )
    return resp["accounts"] if "accounts" in resp else []
# ...existing code...
def _batch_keys_resp(id, resp, exception):
    global current_key_dump
# ...existing code...
def _create_sa_keys(iam, projects, path):
    global current_key_dump
# ...existing code...
def _delete_sas(iam, project):
    sas = _list_sas(iam, project)
# ...existing code...
def serviceaccountfactory(
    credentials="credentials.json",
    token="token_sa.pickle",
    path=None,
    list_projects=False,
    list_sas=None,
    create_projects=None,
    max_projects=12,
    enable_services=None,
    services=["iam", "drive"],
    create_sas=None,
    delete_sas=None,
    download_keys=None,
):
    selected_projects = []
    proj_id = loads(open(credentials, "r").read())["installed"]["project_id"]
# ...existing code...
    cloud = build("cloudresourcemanager", "v1", credentials=creds)
    iam = build("iam", "v1", credentials=creds)
    serviceusage = build("serviceusage", "v1", credentials=creds)
# ...existing code...
    if list_projects:
        return _get_projects(cloud)
    if list_sas:
        return _list_sas(iam, list_sas)
    if create_projects:
        print(f"creat projects: {create_projects}")
# ...existing code...
    if enable_services:
        ste = [enable_services]
# ...existing code...
    if create_sas:
        stc = [create_sas]
# ...existing code...
    if download_keys:
        try:
            os.mkdir(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        std = [download_keys]
# ...existing code...
    if delete_sas:
        std = []
        std.append(delete_sas)
# ...existing code...
if __name__ == "__main__":
    parse = ArgumentParser(description="A tool to create Google service accounts.")
# ...existing code...
    args = parse.parse_args()
    # If credentials file is invalid, search for one.
    if not os.path.exists(args.credentials):
        options = glob("*.json")
# ...existing code...
    if args.quick_setup:
        opt = "~" if args.new_only else "*"
        args.services = ["iam", "drive"]
        args.create_projects = args.quick_setup
        args.enable_services = opt
        args.create_sas = opt
        args.download_keys = opt
    resp = serviceaccountfactory(
        path=args.path,
        token=args.token,
        credentials=args.credentials,
        list_projects=args.list_projects,
        list_sas=args.list_sas,
        create_projects=args.create_projects,
        max_projects=args.max_projects,
        create_sas=args.create_sas,
        delete_sas=args.delete_sas,
        enable_services=args.enable_services,
        services=args.services,
        download_keys=args.download_keys,
    )
    if resp is not None:
        if args.list_projects:
            if resp:
                print("Projects (%d):" % len(resp))
                for i in resp:
                    print(f"  {i}")
            else:
                print("No projects.")
        elif args.list_sas:
            if resp:
                print("Service accounts in %s (%d):" % (args.list_sas, len(resp)))
                for i in resp:
                    print(f"  {i['email']} ({i['uniqueId']})")
            else:
                print("No service accounts.")
