# energyplus-service

[![PyPI - Version](https://img.shields.io/pypi/v/energyplus-service.svg)](https://pypi.org/project/energyplus-service)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/energyplus-service.svg)](https://pypi.org/project/energyplus-service)

-----

**Table of Contents**

- [Installation](#installation)
- [Examples](#examples)
- [License](#license)

## Installation

```console
pip install energyplus-service
```

## Examples

Several examples are provided to test things out. These will work either with the `flask` development server or with `waitress` or `gunicorn` (hopefully). Start up the service with

```console
> energyplus-service dev -e path/to/energyplus.exe
```

or

```console
> scripts/setup-run-env.bat
> waitress-serve --host 127.0.0.1 --port 5000 --call energyplus_service:create_app
```

or

```console
gunicorn version goes here
```

Then the `run-X.py` scripts in the `scripts` subdirectory demonstrate several different ways to use the service.

## License

`energyplus-service` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
