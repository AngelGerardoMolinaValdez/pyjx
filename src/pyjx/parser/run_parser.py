class RunCommandBuilder:
    def __init__(self, subparsers):
        self.subparsers = subparsers

    def build(self):
        run_parser = self.subparsers.add_parser('run', help='Run commands')
        run_subparsers = run_parser.add_subparsers(help='Run subcommands')

        env_parser = run_subparsers.add_parser('env', help='Run environment')
        env_parser.add_argument("--path", "-p", default=None, help='')
        env_parser.set_defaults(func=lambda args: print("Running environment with args:"))

        up_parser = run_subparsers.add_parser('up', help='Run up')
        up_parser.add_argument("--path", "-p", default=None, help='')
        up_parser.set_defaults(func=lambda args: print("Running up with no args needed."))
