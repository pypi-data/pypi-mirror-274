#!/usr/bin/env python
#  buzz [--server URL] [--token TOKEN] list
"""

Buzz client

Usage:
    buzz [options] list
    buzz [options] version
    buzz [options] send <notifier> --recipient <recipient> [--title <title>] [--severity <severity>] [--attach <file>] [<body>...]
    buzz --version


Options:
    -h  --help                   show this help message and exit
    -d
    -q

    -v --version                 show version and exit

    -a URL --api=URL             API URL
    -t TOKEN --token=TOKEN       API Auth token

    --recipient <recipient>      the recipient of the notification,
                                 must be valid for the notifier chosen
    --title <title>              the title of the notification. [default: You received a buzz]
    --severity <severity>        the severity of the message. [default: info]
                                 One of: 'info', 'success', 'warning', 'failure'
    --attach <file>              a file you want to attach to the notification

    <notifier>                   the notifier you want to use,
                                 you can see the available notifiers using `list` command

    <body>                       Content of the notification,
                                 if not specified read from stdin
Environment variables:
    - BUZZ_API         API URL, overrides command line argument
    - BUZZ_TOKEN       API token, overrides command line argument
"""
import sys
import signal
from docopt import docopt
from buzz_client.client import BuzzClient
from scriptonite.configuration import Configuration
from scriptonite.logging import Logger

log = Logger(level="INFO")

VERSION = "1.0.3b"


def shutdown(sig, frame):
    print("\nAye, aye! See you...")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)


def banner(client):
    server_line = f"buzzAPI: {client.api} v.{client.api_version}"
    client_line = f"client version: {VERSION}"

    banner = []
    banner.append(f"# {server_line:^50} #")
    banner.append(f"# {client_line:^50} #")

    header = "#" * len(banner[0])

    print(header)
    print("\n".join(banner))
    print(header)
    print()


def main():
    arguments = docopt(__doc__, version=VERSION)

    if (arguments.get('--debug')):
        print(">> arguments")
        for k, v in arguments.items():
            print(f"{k:15}: {str(v):20}")
        print("")

    client_configuration = Configuration()
    client_configuration.from_mapping(
        dict(api=arguments.get('--api'), token=arguments.get('--token')))
    client_configuration.from_environ(prefix="BUZZ")

    client = BuzzClient(client_configuration)

    if client.api is None or client.settings.token is None:
        print("\n** Missing values for API URL or TOKEN")
        sys.exit(2)

    # Check connection
    check = client.check()
    if not check.get('api_ok'):
        print(f"\nERROR: connection to '{client.api}' failed.\n")
        sys.exit(2)
    if not check.get('token_ok'):
        print(f"\nERROR: authentication failed while connecting to '{
              client.api}'\n")
        sys.exit(3)

    if arguments.version:
        banner(client)
        sys.exit(0)

    if arguments.list:
        print("Available notifiers")
        print("-" * len("Available notifiers"))
        for notifier in client.notifiers:
            print(notifier)
        sys.exit(0)

    if arguments.send:
        if arguments.get('<body>'):
            body = [" ".join(arguments.get('<body>'))]  # type: ignore
        else:
            body = []
            for line in sys.stdin:
                body.append(line)

        if len(body) == 0:
            print("ERROR: refusing to send an empty message\n")
            sys.exit(2)

        r = client.send(notifier=arguments.get('<notifier>'),  # type: ignore
                        title=arguments.get('--title'),  # type: ignore
                        recipient=arguments.get(
            '--recipient'),  # type: ignore
            body="".join(body),
            severity=arguments.get('--severity'),  # type: ignore
            attach=arguments.get('--attach')  # type: ignore
        )
        print(f"{r.json().get('detail')} [{r.status_code}]")

        sys.exit(int(not (r)))


if __name__ == "__main__":
    main()
