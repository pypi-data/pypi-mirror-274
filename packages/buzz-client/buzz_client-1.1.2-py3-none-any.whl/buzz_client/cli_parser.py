import argparse

import importlib.metadata

VERSION = importlib.metadata.version("buzz_client")

epilogue = """
environment variables:
    - BUZZ_API         API URL, overrides command line argument

API URL format is `http(s)://auth-token@server`
Example: http://sesame@localhost:8000
"""


class Formatter(argparse.RawDescriptionHelpFormatter,
                argparse.ArgumentDefaultsHelpFormatter):
    """
    We want to show the default values and show the description
    and epilogue not reformatted, so we create our own formatter class
    """
    pass


parser = argparse.ArgumentParser(prog="buzz",
                                 description="A client for buzzAPI",
                                 epilog=epilogue,
                                 formatter_class=Formatter)

# parser.add_argument('--verbose', '-v',
#                     help="verbosity level",
#                     action='count',
#                     default=0)

parser.add_argument('-a', '--api', type=str,
                    help="the URL of the API server")
parser.add_argument('--version', action='version',
                    version=f'%(prog)s {VERSION}')


sub = parser.add_subparsers(title="commands", required=True)

list_group = sub.add_parser(name="list",
                            description="List available notifiers",
                            help='list available notifiers',
                            epilog=epilogue,
                            formatter_class=Formatter)
list_group.set_defaults(action="list")

version_group = sub.add_parser(name="version",
                               description="Show client and server versions",
                               help='show client and server versions',
                               epilog=epilogue,
                               formatter_class=Formatter)
version_group.set_defaults(action="version")


send_group = sub.add_parser(name="send",
                            description="Send a notification",
                            help='send a notification',
                            epilog=epilogue,
                            formatter_class=Formatter)
send_group.set_defaults(action="send")

send_group.add_argument('notifier', type=str,
                        metavar='<notifier>',
                        help='the notifier to use')

send_group.add_argument('recipient', type=str,
                        metavar='<recipient>',
                        help='the recipient of the notification, '
                        'format depends on notifier')

send_group.add_argument('body',
                        metavar='<body>',
                        nargs='*',
                        # action="append",
                        # type=argparse.FileType('r'),
                        type=str,
                        help='the content of the notification, '
                        'if empty it is read from standard input')

send_group.add_argument('-t', '--title', type=str,
                        help='the title',
                        default="You received a buzz")

send_group.add_argument('-f', '--format', type=str,
                        help='the format of the body',
                        choices=['text', 'html', 'markdown'],
                        default="text")

send_group.add_argument('-s', '--severity', type=str,
                        help='severity of the message',
                        choices=['info',
                                 'success',
                                 'warning',
                                 'critical'],
                        default="info")


send_group.add_argument('-a', '--attach', type=str,
                        help='the filename to attach')
