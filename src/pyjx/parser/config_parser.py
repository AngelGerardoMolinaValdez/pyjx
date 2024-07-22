class ConfigCommandBuilder:
    def __init__(self, subparsers):
        self.subparsers = subparsers

    def build(self):
        config_parser = self.subparsers.add_parser('config', help='Configuration settings')
        config_parser.set_defaults(func=lambda args: print("Coming soon..."))
