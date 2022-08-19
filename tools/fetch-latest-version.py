#!/usr/bin/env python
"""Fetch version string from latest release
"""
import argparse
import configparser
import sys
from pathlib import Path

from github import Github


def fetch_latest_version(path: str) -> str:
    g = Github()
    repo = g.get_repo(path)
    release = repo.get_latest_release()
    return release.tag_name


class Arguments:
    config: str
    context: Path

    def resolve(self):
        self.context = (Path.cwd() / self.context).resolve()
        self.config = (self.context / self.config).resolve()
        if not self.config.exists():
            raise ValueError("--config is not exists")
        if not self.config.is_file():
            raise ValueError("--config is not file")


def main(args: Arguments) -> int:
    cfg = configparser.ConfigParser()
    cfg.read(args.config)
    latest = fetch_latest_version(cfg.get("main", "repo"))
    current = cfg.get("main", "version")
    print(f"::set-output name=latest::{latest}")
    print(f"::set-output name=current::{current}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="package.ini")
    parser.add_argument("context", nargs="?", default=".")

    try:
        args = parser.parse_args(namespace=Arguments())
        args.resolve()
        ret = main(args)
    except ValueError as err:
        print(err)
        ret = 1
    sys.exit(ret)
