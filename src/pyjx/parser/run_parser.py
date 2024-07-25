from workflows.env.environment_command import EnvironmentCommand

class RunCommandBuilder:
    def __init__(self, subparsers):
        self.subparsers = subparsers

    def build(self):
        run_parser = self.subparsers.add_parser('run', help='Run commands')
        run_subparsers = run_parser.add_subparsers(help='Run subcommands')

        env_parser = run_subparsers.add_parser('env', help='Run environment')
        env_parser.add_argument("--path", "-p", default=None, help='')
        env_parser.add_argument("--txt-reporter", "-tr", action="store_true", help='')
        env_parser.add_argument("--no-console-reporter", "-ncr", action="store_true", default=False, help='')
        env_parser.add_argument("--schema-version", "-sv", default=1, type=int, help='')
        env_parser.set_defaults(namespace="pyjx.env.json")
        env_parser.set_defaults(func=lambda args, invoke_path: EnvironmentCommand(args, invoke_path).execute())

        up_parser = run_subparsers.add_parser('up', help='Run up')
        up_parser.add_argument("--path", "-p", default=None, help='')
        up_parser.add_argument("--txt-reporter", "-tr", action="store_true", help='')
        up_parser.add_argument("--no-console-reporter", "-ncr", action="store_false", help='')
        up_parser.add_argument("--schema-version", "-sv", default=1, type=int, help='')
        up_parser.set_defaults(namespace="pyjx.up.json")
        up_parser.set_defaults(func=lambda args: print("Running up with no args needed."))
