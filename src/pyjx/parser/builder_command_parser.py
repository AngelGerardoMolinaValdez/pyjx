import argparse
from .run_parser import RunCommandBuilder
from .config_parser import ConfigCommandBuilder
from .init_parser import InitCommandBuilder

class CommandBuilder:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PYJX2 CLI Tool")
        self.subparsers = self.parser.add_subparsers(help='commands', dest='command')

    def build_run_command(self):
        run_builder = RunCommandBuilder(self.subparsers)
        run_builder.build()

    def build_config_command(self):
        config_builder = ConfigCommandBuilder(self.subparsers)
        config_builder.build()

    def build_init_command(self):
        config_builder = InitCommandBuilder(self.subparsers)
        config_builder.build()

    def get_parser(self):
        return self.parser
