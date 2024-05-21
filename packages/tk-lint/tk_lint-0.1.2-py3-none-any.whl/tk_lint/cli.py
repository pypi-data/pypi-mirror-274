import os
import subprocess
import sys

import click


@click.group()
def tk_lint_cli():
    print("Running tk_lint")


@tk_lint_cli.command()
@click.argument("paths", required=False, nargs=-1)
def ruff(paths):
    if len(paths) == 0:
        paths = ['.']

    relative_dir = os.path.dirname(__file__)
    toml_config_path = relative_dir + "/config/ruff.toml"
    process = subprocess.Popen(["ruff", "check", *paths, "--config", toml_config_path])
    process.communicate()
    sys.exit(process.returncode)
