# AI Project Template

[![Build](https://github.com/felixpeters/ai-project-template/actions/workflows/ci.yml/badge.svg)](https://github.com/felixpeters/ai-project-template/actions/workflows/ci.yml)

Template for developing AI projects according to [proven principles](https://fullstackai.substack.com/p/four-pillars-ai-development) and best practices.

## Features

- Proven folder structure for AI projects
- Template notebooks for the minimum viable product (MVP) of an AI project
- Continuous integration with GitHub Actions
- Pre-commit hooks for code quality, style, and security (black, ruff, codespell, bandit)
- Testing with pytest, including code coverage

## Setup

### Prerequisites

- Python 3.10
- Make

### Installation process

- Create a new repository from this template using `gh repo create <repo-name> --template felixpeters/ai-project-template`
- Create a Python environment with `python -m venv .venv`
- Activate the environment with `source .venv/bin/activate`
- Install the development dependencies with `pip install -r requirements-dev.txt`
- Install the pre-commit hooks with `pre-commit install`
- Install the project in editable mode with `make build`
- Make sure all tests pass with `make test`
- Create a data directory with `mkdir data`

## Usage

### Repository structure

The repository is structured as follows:

- `.github/`: Contains GitHub Actions workflows for continuous integration.
- `data/`: Contains all data used in the project
- `docs/`: Contains documentation for the project
- `src/`: Contains the source code of the project
- `tests/`: Contains the tests for the project
- `mvp/`: Contains the minimum viable product of the project, i.e., an end-to-end pipeline for running experiments
- `Makefile`: Contains commands for building, testing, and running the project
- `requirements.txt`: Contains the dependencies of the project
- `requirements-dev.txt`: Contains the development dependencies of the project
- `setup.py`: Contains instructions for building the project package
- `pyproject.toml`: Contains configuration for Python development standards

### Workflows

| ID   | Description                                                    | Trigger               |
| ---- | -------------------------------------------------------------- | --------------------- |
| `ci` | Installs dependencies, builds the packagage and runs all tests | Push to `main` branch |

## Roadmap

- [ ] Add common utility functions (load configuration, logging, etc.)
- [ ] Add Dockerfile for VS Code Dev Container as alternative dev environment
