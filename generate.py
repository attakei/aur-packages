#!/usr/bin/env python
import argparse
import hashlib
import sys
from pathlib import Path

import httpx
import jinja2

TEMPLATE_DIR = Path(__file__).parent / "templates"

parser = argparse.ArgumentParser()
parser.add_argument("version")
parser.add_argument("dist")


def source_bin(version: str) -> dict:
    url = f"https://github.com/firebase/firebase-tools/releases/download/v{version}/firebase-tools-linux"
    resp = httpx.get(url, follow_redirects=True)
    checksum = hashlib.md5(resp.content).hexdigest()
    return {
        "bin_url": url,
        "bin_checksum": checksum,
    }


def source_license(version: str) -> dict:
    url = f"https://github.com/firebase/firebase-tools/raw/v{version}/LICENSE"
    resp = httpx.get(url, follow_redirects=True)
    checksum = hashlib.md5(resp.content).hexdigest()
    return {
        "license_url": url,
        "license_checksum": checksum,
    }


def main(args: argparse.Namespace) -> int:
    ctx = {
        "version": args.version,
    }
    ctx.update(source_bin(args.version))
    ctx.update(source_license(args.version))

    dist = Path(args.dist)
    dist.mkdir(parents=True, exist_ok=True)
    pkgbuild_template = jinja2.Template((TEMPLATE_DIR / "PKGBUILD.j2").read_text())
    (dist / "PKGBUILD").write_text(pkgbuild_template.render(**ctx))
    srcinfo_template = jinja2.Template((TEMPLATE_DIR / "SRCINFO.j2").read_text())
    (dist / ".SRCINFO").write_text(srcinfo_template.render(**ctx))
    return 0


if __name__ == "__main__":
    args = parser.parse_args()
    sys.exit(main(args))
