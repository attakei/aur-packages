#!/usr/bin/env python
"""Proc to update source version of package.

- Fetch version string from latest release
- Update package.ini
"""
import argparse
import sys
from pathlib import Path

import tomli
import tomli_w
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
        return self.target / "package.toml"


def main(args: Arguments) -> int:
    cfg = tomli.loads(args.config.read_text())
    latest = fetch_latest_version(cfg["main"]["repo"])
    current = cfg["main"]["version"]
    print(f"::set-output name=latest::{latest}")
    print(f"::set-output name=current::{current}")
    if current != latest:
        cfg["main"]["version"] = latest
        cfg["main"]["release"] = 1
        args.config.write_text(tomli_w.dumps(cfg))
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
