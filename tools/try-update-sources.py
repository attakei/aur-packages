#!/usr/bin/env python
"""Proc to update source version of package.

- Fetch version string from latest release
- Update package.ini
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
    target: Path

    def resolve(self):
        self.target = (Path.cwd() / self.target).resolve()
        if self.config.exists() and self.config.is_file():
            pass
        else:
            raise ValueError("Invalid target")

    @property
    def config(self) -> Path:
        return self.target / "package.ini"


def main(args: Arguments) -> int:
    cfg = configparser.ConfigParser()
    cfg.read(args.config)
    latest = fetch_latest_version(cfg.get("main", "repo"))
    current = cfg.get("main", "version")
    print(f"::set-output name=latest::{latest}")
    print(f"::set-output name=current::{current}")
    if current != latest:
        cfg["main"]["version"] = latest
        with args.config.open("w") as fp:
            cfg.write(fp)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target")

    try:
        args = parser.parse_args(namespace=Arguments())
        args.resolve()
        ret = main(args)
    except ValueError as err:
        print(err)
        ret = 1
    sys.exit(ret)
