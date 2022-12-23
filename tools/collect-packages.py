#!/usr/bin/env python
import argparse
import json
import sys
from pathlib import Path


class Arguments:
    root: Path

    def resolve(self):
        self.root = (Path.cwd() / self.root).resolve()
        if not self.root.exists():
            raise ValueError("ROOT is not exists")
        if not self.root.is_dir():
            raise ValueError("ROOT is not directory")


def main(args: Arguments) -> int:
    packages = [
        p.name
        for p in args.root.glob("*")
        if p.is_dir() and (p / "package.toml").exists()
    ]
    output = json.dumps(packages)
    print(f"::set-output name=packages::{output}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root")

    try:
        args = parser.parse_args(namespace=Arguments())
        args.resolve()
        ret = main(args)
    except ValueError as err:
        print(err)
        ret = 1
    sys.exit(ret)
