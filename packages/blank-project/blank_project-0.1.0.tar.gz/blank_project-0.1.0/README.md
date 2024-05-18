# blank-project

<!-- ![Build Status](https://github.com/<username>/<reponame>/actions/workflows/ci.yaml/badge.svg?branch=master) -->
<!-- ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/<reponame>) -->
<!-- ![PyPI Version](https://img.shields.io/pypi/v/<reponame>) -->
<!-- [![Code Coverage](https://codecov.io/gh/<username>/<reponame>/graph/badge.svg?token=<token>)](https://codecov.io/gh/<username>/<reponame>) -->
<!-- [![Maintainability](https://api.codeclimate.com/v1/badges/<id>/maintainability)](https://codeclimate.com/github/<username>/<reponame>/maintainability) -->

A dummy package for quickly starting typical Python projects.

Features:

* Basic `.gitignore`;
* GitHub actions for builds and checks;
* Acceptable directory structure at once;
* Regular automation based on a `Makefile`;
* Templates for basic python badges into `README.md`.
* Single point of project specification - `pyproject.toml`;
* Acceptable settings for: `black`, `isort`, `flake8`, `mypy`, `pydocstyle` and `coverage`;

## Usage

1. Clone repo:

```shellsession
$ git clone https://github.com/p3t3rbr0/py3-blank-project.git
```

2. Rename project directory name on your choice:

```shellsession
$ mv py3-blank-project <py3-project-name>
```

3. Run **init.sh** with your project name:

```shellsession
$ cd <py3-project-name>
$ NAME=<project-name> ./init.sh
```

4. Remove **init.sh**

```shellsession
$ rm -f init.sh
```

5. Change `authors`, `description`, `keywords` and `classifiers` into **pyproject.toml**.

6. Change `README.md`, `CHANGELOG.md` and `LICENSE` files.

A new blank python project is ready, create gh-repo and go forward!

## Available make commands

### Dependencies

- `make deps-dev` - Install only development dependencies.
- `make deps-build` - Install only build system dependencies.
- `make deps` - Install all dependencies.

### Distributing

- `make build-sdist` - Build a source distrib.
- `make build-wheel` - Build a pure python wheel distrib.
- `make build` - Build both distribs (source and wheel).
- `make upload` - Upload built packages to PyPI.

### Development

- `make cleanup` - Clean up python temporary files and caches.
- `make format` - Fromat the code (by black and isort).
- `make lint` - Check code style, docstring style and types (by flake8, pydocstyle and mypy).
- `make tests` - Run tests with coverage measure (output to terminal).
- `make tests-cov-json` - Run tests with coverage measure (output to json [coverage.json]).
- `make tests-cov-html` - Run tests with coverage measure (output to html [coverage_report/]).
