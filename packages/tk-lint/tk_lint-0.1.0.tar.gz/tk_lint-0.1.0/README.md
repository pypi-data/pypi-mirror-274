# TK Lint


TK Lint is a package/CLI the includes different linting rules such as Ruff, MyPy, etc.. to be used as a standard across repositories. It's built using [poetry](https://python-poetry.org/)

This repository is still WIP.

### Setup
* Install [pipx](https://pipx.pypa.io/stable/installation/) on your machine
* Install poetry using pipx `pipx install poetry`

### Install
- To install dependencies, run `make install`
- To run poetry shell, run `make shell`
- To use ruff, run `tk_lint ruff <path>` within the shell
