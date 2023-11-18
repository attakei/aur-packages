#!/usr/bin/env python
"""Generate resources of package in AUR.
"""
import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

import httpx
import jinja2
import tomli


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
    name: str
    url: str
    checksum: str

    @classmethod
    def load(cls, name: str, url: str) -> "Source":
        resp = httpx.get(url, follow_redirects=True)
        checksum = hashlib.md5(resp.content).hexdigest()
        return cls(name=name, url=url, checksum=checksum)


def main(args: Arguments) -> int:
    cfg = tomli.loads((args.root / "package.toml").read_text())
    ctx = {
        "version": cfg["main"]["version"],
        "release": cfg["main"]["release"],
        "depends": cfg["main"].get("depends", None),
        "sources": [],
    }
    print(f"::set-output name=version::{ctx['version']}")
    ctx["version_text"] = ctx["version"][1:]
    for source in cfg["sources"]:
        src = Source.load(source["name"], source["url"].format(**ctx))
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
