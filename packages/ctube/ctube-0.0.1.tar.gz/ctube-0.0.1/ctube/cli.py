from argparse import ArgumentParser
from ctube.config import config
from ctube.app import App


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="ctube",
        description="Download music from the command line"
    )
    return parser


def main() -> None:
    # parser = get_parser()
    app = App(
        output_path=config["output_path"],
        skip_existing=config["skip_existing"]
    )
    app.main_loop()


if __name__ == "__main__":
    main()
