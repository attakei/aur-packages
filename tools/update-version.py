#!/usr/bin/env python
"""Fetch version string from latest release
"""
import argparse
import configparser
import sys
from pathlib import Path


class Arguments:
    config: Path
    version: str

    def resolve(self):
        self.config = (Path.cwd() / self.config).resolve()
        if not self.config.exists():
            raise ValueError("--config is not exists")
        if not self.config.is_file():
            raise ValueError("--config is not file")


def main(args: Arguments) -> int:
    cfg = configparser.ConfigParser()
    cfg.read(args.config)
    cfg["main"]["version"] = args.version
    with args.config.open("w") as fp:
        cfg.write(fp)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="package.ini")
    parser.add_argument("version")

    try:
        args = parser.parse_args(namespace=Arguments())
        args.resolve()
        ret = main(args)
    except ValueError as err:
        print(err)
        ret = 1
    sys.exit(ret)
