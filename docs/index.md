<p>
    <a href="https://github.com/data-dev/DataReactor/actions" alt="Github Actions">
        <img src="https://img.shields.io/github/workflow/status/data-dev/DataReactor/Run%20Tests" /></a>
    <a href="https://codecov.io/gh/data-dev/DataReactor" alt="Code Coverage">
        <img src="https://codecov.io/gh/data-dev/DataReactor/branch/master/graph/badge.svg" /></a>
    <a href="https://github.com/data-dev/DataReactor/pulse" alt="Commit Activity">
        <img src="https://img.shields.io/github/commit-activity/m/data-dev/DataReactor" /></a>
</p>


# Overview
Augmenting relational datasets by generating derived columns with known lineage.

- Documentation: https://data-dev.github.io/DataReactor
- Homepage: https://github.com/data-dev/DataReactor

# Installation

## Requirements

**DataReactor** has been developed and tested on [Python 3.5, 3.6, 3.7 and 3.8](https://www.python.org/downloads/)

Also, although it is not strictly required, the usage of a [virtualenv](https://virtualenv.pypa.io/en/latest/)
is highly recommended in order to avoid interfering with other software installed in the system
in which **DataReactor** is run.

These are the minimum commands needed to create a virtualenv using python3.6 for **DataReactor**:

```bash
pip install virtualenv
virtualenv -p $(which python3.6) DataReactor-venv
```

Afterwards, you have to execute this command to activate the virtualenv:

```bash
source DataReactor-venv/bin/activate
```

Remember to execute it every time you start a new console to work on **DataReactor**!

<!-- Uncomment this section after releasing the package to PyPI for installation instructions
## Install from PyPI

After creating the virtualenv and activating it, we recommend using
[pip](https://pip.pypa.io/en/stable/) in order to install **DataReactor**:

```bash
pip install datareactor
```

This will pull and install the latest stable release from [PyPI](https://pypi.org/).
-->

## Install from source

With your virtualenv activated, you can clone the repository and install it from
source by running `make install` on the `stable` branch:

```bash
git clone git@github.com:data-dev/DataReactor.git
cd DataReactor
git checkout stable
make install
```

## Install for Development

If you want to contribute to the project, a few more steps are required to make the project ready
for development.

Please head to the [Contributing Guide](https://data-dev.github.io/DataReactor/contributing.html#get-started)
for more details about this process.
