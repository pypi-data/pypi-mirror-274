import os
import subprocess
import sys

import click


@click.group()
def tk_lint_cli():
    print("Running tk_lint")


@tk_lint_cli.command()
@click.argument("path", required=False)
def ruff(path):
    if path is None:
        path = "."

    relative_dir = os.path.dirname(__file__)
    toml_config_path = relative_dir + "/ruff.toml"
    process = subprocess.Popen(["ruff", "check", path, "--config", toml_config_path])
    process.communicate()
    sys.exit(process.returncode)
