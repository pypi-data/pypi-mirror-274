import os
import random
import readline
import requests
import configparser
import docmesh_cli

from typing import Any

from packaging.version import Version
from docmesh_cli.logos import LOGOS


RC_FILE = os.path.expanduser("~/.docmeshrc")
PARSER = configparser.ConfigParser()

ADMIN_SHORTCUTS = {
    "/add_entity": {
        "path": "/admin/add_entity",
        "args": "entity_name",
        "description": "add a new entity, usage: /add_entity ENTITY_NAME",
    },
    "/update": {
        "path": "/embeddings/update",
        "args": "",
        "description": "update papers embeddings, usage: /update",
    },
}

SHORTCUTS = {
    "/add": {
        "path": "/papers/add",
        "args": "paper",
        "description": "add a new paper, usage: /add PAPER_TITLE/ARXIV_ID",
    },
    "/mark": {
        "path": "/papers/add_and_mark",
        "args": "paper",
        "description": "add and mark a paper read, usage: /mark PAPER_TITLE/ARXIV_ID",
    },
    "/help": {
        "description": "show this help menu",
    },
    "/clear": {
        "description": "clear the session memory",
    },
    "/end": {
        "description": "exit query",
    },
    "/exit": {
        "description": "exit query",
    },
}


class TermColor:
    blue = "\033[94m"
    green = "\033[92m"
    red = "\033[96m"
    end = "\033[0m"


def _check_verseion():
    current_version = Version(docmesh_cli.__version__)

    # get latest version from pypi
    pypi_link = f"https://pypi.org/pypi/{docmesh_cli.__name__}/json"
    rsp = requests.get(pypi_link, timeout=30)

    if rsp.status_code == 200:
        latest_version = Version(rsp.json()["info"]["version"])
        if current_version < latest_version:
            print(
                f"{TermColor.red}Current client version is {current_version}, the latest verision is {latest_version}."
                f"You could update the client version using `pip install -U {docmesh_cli.__name__}`. {TermColor.end}"
            )
        else:
            print(f"{TermColor.green}Using the latest client version!{TermColor.end}")
    else:
        print(f"{TermColor.red}Check latest client version failed.{TermColor.end}")


def _create_profile() -> tuple[str, str]:
    server = input("docmesh server: ")
    access_token = input("docmesh token: ")
    profile = input("profile name: ")

    PARSER[profile] = {}
    PARSER[profile]["server"] = server
    PARSER[profile]["access_token"] = access_token

    with open(RC_FILE, "w", encoding="utf-8") as f:
        PARSER.write(f)

    return server, access_token


def _profile_management() -> tuple[str, str]:
    if not os.path.exists(RC_FILE):
        print(f"You have not set up {RC_FILE}, create a new profile.")
        return _create_profile()
    else:
        print(f"Load profiles from {RC_FILE}.")
        PARSER.read(RC_FILE)

        profiles: dict[int, str] = dict(enumerate(PARSER.sections()))
        msg = "\n".join(f"{k}: {v}" for k, v in profiles.items())

        print(msg)
        option = int(input("Select you profile (if selection is not available, you can create a new profile): "))

        if option in profiles:
            server = PARSER[profiles[option]]["server"]
            access_token = PARSER[profiles[option]]["access_token"]

            return server, access_token
        else:
            return _create_profile()


def _show_shortcut() -> str:
    help_menu = [f"{k}, {SHORTCUTS[k]['description']}" for k in SHORTCUTS]
    return "\n".join(help_menu)


def _shortcut(
    server: str,
    path: str,
    headers: dict[str, str],
    **kwargs: dict[str, Any],
) -> None:
    url = f"{server}{path}"
    rsp = requests.post(url=url, headers=headers, json=kwargs, timeout=300)

    if rsp.status_code == 401:
        print(f"{TermColor.red}Unauthorized to execute this shortcut.{TermColor.end}")
        raise ValueError()
    else:
        msg = rsp.json()["data"]["msg"]

        if rsp.status_code == 200:
            print(f"{TermColor.green}{msg}{TermColor.end}")
        else:
            print(f"{TermColor.red}{msg}{TermColor.end}")


def _login(
    server: str,
    headers: dict[str, str],
    clear: bool = False,
) -> tuple[str, str]:
    rsp = requests.post(url=f"{server}/login", headers=headers, timeout=300)

    if rsp.status_code == 200:
        data = rsp.json()["data"]
        entity_name = data["entity_name"]
        session_id = data["session_id"]
        if not clear:
            print(f"{TermColor.green}You are logined in as: {entity_name} at {server}{TermColor.end}")
    elif rsp.status_code == 401:
        detail = rsp.json()["detail"]
        print(f"{TermColor.red}{detail}{TermColor.end}")
        rsp.raise_for_status()
    else:
        rsp.raise_for_status()

    return session_id


def client() -> None:
    print(random.choice(LOGOS))

    # check client version
    _check_verseion()

    # load server and access_token from profiles
    server, access_token = _profile_management()

    # setup headers
    headers = {"Authorization": f"Bearer {access_token}"}

    # retreive session_id
    session_id = _login(server, headers, clear=False)

    # switch on/off streaming mode
    streaming = input(f"{TermColor.red}Streaming mode [y/n]: {TermColor.end}")
    if streaming.lower() == "y":
        streaming = True
    elif streaming.lower() == "n":
        streaming = False
    else:
        print(f"You enter an invalid option {streaming}, turn off streaming mode.")
        streaming = False

    # send query
    while True:
        query = input(f"{TermColor.blue}query: {TermColor.end}")

        if query.startswith("/"):
            # trigger shortcut
            if query == "/help":
                print(f"{TermColor.green}{_show_shortcut()}{TermColor.end}")
                continue
            if query == "/clear":
                # retreive entity_name and session_id again
                session_id = _login(server, headers, clear=True)
                print(f"{TermColor.green}Successfully cleared session memory.{TermColor.end}")
                continue

            if query in ("/end", "/exit"):
                break

            try:
                query_splitted = query.split(" ")
                if len(query_splitted) == 1:
                    shortcut_cmd, shortcut_args = query_splitted[0], None
                else:
                    shortcut_cmd, shortcut_args = query_splitted[0], " ".join(query_splitted[1:])

                if shortcut_cmd in ADMIN_SHORTCUTS:
                    path, args = ADMIN_SHORTCUTS[shortcut_cmd]["path"], ADMIN_SHORTCUTS[shortcut_cmd]["args"]
                elif shortcut_cmd in SHORTCUTS:
                    path, args = SHORTCUTS[shortcut_cmd]["path"], SHORTCUTS[shortcut_cmd]["args"]
                else:
                    print(f"{TermColor.red}You enter an invalid shortcut {query}\n{_show_shortcut()}{TermColor.end}")
                    continue

                if args == "":
                    shortcut_kwargs = {}
                else:
                    shortcut_kwargs = {args: shortcut_args}
                _shortcut(server, path, headers, **shortcut_kwargs)
            except Exception:
                print(f"{TermColor.red}You enter an invalid shortcut {query}\n{_show_shortcut()}{TermColor.end}")
                continue
        else:
            data = {"session_id": session_id, "query": query}
            if streaming:
                chunks: list[bytes] = []
                with requests.post(
                    url=f"{server}/agents/aexecute", headers=headers, json=data, stream=True, timeout=300
                ) as r:
                    for chunk in r.iter_content(chunk_size=64):
                        # some special symbol may be splitted by chunk size
                        # so we use a temporal chunks to store these part
                        # and we will try to decode these chunks asap
                        chunks.append(chunk)
                        try:
                            s = b"".join(chunks).decode()
                            chunks = []
                            print(s, end="", flush=True)
                        except UnicodeDecodeError:
                            continue
            else:
                rsp = requests.post(url=f"{server}/agents/execute", headers=headers, json=data, timeout=300)
                msg = rsp.json()["data"]["msg"]
                print(msg, end="", flush=True)
