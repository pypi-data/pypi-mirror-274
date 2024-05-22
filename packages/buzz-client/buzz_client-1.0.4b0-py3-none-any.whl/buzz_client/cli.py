#!/usr/bin/env python
#  buzz [--server URL] [--token TOKEN] list
"""

Buzz client

Usage:
    buzz [options] list
    buzz [options] version
    buzz [options] send <notifier> <recipient> [--title <title>] [--severity <severity>] [--attach <file>] [<body>...]
    buzz --version

Arguments:
    <notifier>                   the notifier you want to use, you can see the available notifiers using `list` command
    <recipient>                  the recipient of the notification, must be valid for the notifier chosen
    <body>                       Content of the notification, if not specified read from stdin

Options:

    -h  --help                   show this help message and exit

    -v --version                 show version and exit

    -a URL --api=URL             API URL

    --title <title>              the title of the notification. [default: You received a buzz]
    --severity <severity>        the severity of the message. [default: info]
                                 One of: 'info', 'success', 'warning', 'failure'
    --attach <file>              a file you want to attach to the notification
    --format <format>            format of the message text [default: text]
                                 One of: 'text', 'markdown', 'html'

Environment variables:
    - BUZZ_API         API URL, overrides command line argument
                       API URL format is `http(s)://auth-token@server`
                       Example: http://sesame@localhost:8000

"""
import sys
import signal
import time
from docopt import docopt
from buzz_client.client import BuzzClient
from scriptonite.configuration import Configuration
from scriptonite.logging import Logger

log = Logger(level="INFO")

VERSION = "1.0.4"


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


def parse_settings(settings):
    url = settings.api

    if url:
        scheme, rest = url.split(':', 1)
        dirty_token, host = rest.split('@', 1)
        token = dirty_token.replace('/', '')
        return (token, f"{scheme}://{host}")
    else:
        return (None, None)


def main():
    arguments = docopt(__doc__, version=VERSION)

    client_configuration = Configuration()
    # Pass the `--api` argument
    client_configuration.from_mapping(
        dict(api=arguments.get('--api')))
    # Read environment variables
    # We check if we have an `BUZZ_API` env var defined
    # This can override the `--api` value
    client_configuration.from_environ(prefix="BUZZ")

    # Extract token and URL from the API value
    token, url = parse_settings(client_configuration)

    # Bail out on missing parameters
    if url is None or token is None:
        print("\n** Missing values for API URL or TOKEN")
        sys.exit(2)

    # Create the client
    client = BuzzClient(url, token)

    # Check connection
    # Measure round trip time
    start = time.time()
    check = client.check()
    rtt = int((time.time() - start) * 1000)  # in milliseconds

    if not check.get('api_ok'):
        print(f"\nERROR: connection to '{client.api}' failed.\n")
        sys.exit(2)

    if not check.get('token_ok'):
        print(f"\nERROR: authentication failed connecting to '{client.api}'\n")
        sys.exit(3)

    print(f"Connection ok [{rtt}ms]\n")

    if arguments.version:
        # Show banner
        banner(client)
        sys.exit(0)

    if arguments.list:
        # Show available notifiers
        print("Available notifiers")
        print("-" * len("Available notifiers"))
        for notifier in client.notifiers:
            print(notifier)
        sys.exit(0)

    if arguments.send:
        # Send message
        if arguments.get('<body>'):
            body = [" ".join(arguments.get('<body>'))]  # type: ignore
        else:
            body = []
            print("Type your message, <Ctrl-D> to end, <Ctrl-C> to send\n")
            for line in sys.stdin:
                body.append(line)

        if len(body) == 0:
            print("ERROR: refusing to send an empty message\n")
            sys.exit(2)

        r = client.send(notifier=arguments.get('<notifier>'),  # type: ignore
                        title=arguments.get('--title'),
                        recipient=arguments.get('<recipient>'),  # type: ignore
                        body="".join(body),
                        severity=arguments.get('--severity'),
                        attach=arguments.get('--attach'),
                        format_=arguments.get('--format')
                        )
        print(f"{r.json().get('detail')} [{r.status_code}]")

        sys.exit(int(not (r.ok)))


if __name__ == "__main__":
    main()
