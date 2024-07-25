from pyjx.config.auth import SetAuthCommand

class ConfigCommandBuilder:
    def __init__(self, subparsers):
        self.subparsers = subparsers

    def build(self):
        config_parser = self.subparsers.add_parser('config', help='Configuration settings')
        config_subparsers = config_parser.add_subparsers(help="Config commands")

        auth_parser = config_subparsers.add_parser('auth', help='Authentication settings')
        auth_parser.add_argument('username', type=str, help='Username for authentication')
        auth_parser.add_argument('password', type=str, help='Password for authentication')
        auth_parser.set_defaults(func=lambda args: SetAuthCommand(args.username, args.password).execute())
