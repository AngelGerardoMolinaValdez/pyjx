import os
from pyjx.parser.builder_command_parser import CommandBuilder

def main():
    builder = CommandBuilder()
    builder.build_run_command()
    builder.build_config_command()
    builder.build_init_command()
    parser = builder.get_parser()

    args = parser.parse_args()
    if args.command == "run":
        args.func(args, os.getcwd())
    else:
        args.func(args)

if __name__ == "__main__":
    main()
