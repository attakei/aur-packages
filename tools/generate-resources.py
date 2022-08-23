#!/usr/bin/env python
"""Generate resources of package in AUR.
"""
import argparse
import configparser
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

import httpx
import jinja2


class Arguments:
    root: Path
    dist: Path

    def resolve(self):
        self.root = (Path.cwd() / self.root).resolve()
        if not self.root.exists():
            raise ValueError("ROOT is not exists")
        if not self.root.is_dir():
            raise ValueError("ROOT is not directory")
        self.dist = (Path.cwd() / self.dist).resolve()
        if not self.root.exists():
            raise ValueError("DIST is not exists")
        if not self.root.is_dir():
            raise ValueError("DIST is not directory")


@dataclass
class Source:
    url: str
    checksum: str

    @classmethod
    def load(cls, url: str) -> "Source":
        resp = httpx.get(url, follow_redirects=True)
        checksum = hashlib.md5(resp.content).hexdigest()
        return cls(url=url, checksum=checksum)


def main(args: Arguments) -> int:
    cfg = configparser.ConfigParser()
    cfg.read(args.root / "package.ini")
    ctx = {
        "version": cfg.get("main", "version"),
        "sources": [],
    }
    print(f"::set-output name=version::{ctx['version']}")
    ctx["version_text"] = ctx["version"][1:]
    for name, url in cfg.items("sources"):
        src = Source.load(url.format(**ctx))
        ctx["sources"].append(src)
    for template in (args.root / "templates").glob("*.j2"):
        t = jinja2.Template(template.read_text())
        dist = args.dist / template.stem
        dist.write_text(t.render(**ctx))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("dist")

    try:
        args = parser.parse_args(namespace=Arguments())
        args.resolve()
        ret = main(args)
    except ValueError as err:
        print(err)
        ret = 1
    sys.exit(ret)
