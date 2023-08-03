# Case study: Credit card fraud detection

[![Build](https://github.com/felixpeters/fraud-detection/actions/workflows/ci.yml/badge.svg)](https://github.com/felixpeters/fraud-detection/actions/workflows/ci.yml)
[![Visualize in W&B](https://raw.githubusercontent.com/wandb/assets/main/wandb-github-badge-gradient.svg)](https://wandb.ai/felixpeters/fraud-detection)

Template for developing AI projects according to [proven principles](https://fullstackai.substack.com/p/four-pillars-ai-development) and best practices

## Business case

Good case studies on this subject from major tech companies:

- [How we built Stripe Radar](https://stripe.com/blog/how-we-built-it-stripe-radar) (Stripe)
- [Deploying Large-scale Fraud Detection Machine Learning Models at PayPal](https://medium.com/paypal-tech/machine-learning-model-ci-cd-and-shadow-platform-8c4f44998c78) (PayPal)


## Setup

### Prerequisites

- Python 3.10
- Make

### Installation process

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
