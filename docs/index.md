# DataReactor

Augmenting relational datasets by generating derived columns with known lineage.

- Documentation: https://data-dev.github.io/DataReactor
- Homepage: https://github.com/data-dev/DataReactor

# Install

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

# Quickstart

In this short tutorial we will guide you through a series of steps that will help you
getting started with **DataReactor**.

## Prepare a dataset
A few example datasets can be found in the `datasets` directory. To prepare your
own datasets, you can use the [metad](https://github.com/data-dev/MetaData) 
library. Datasets are expected to follow the `metad` format which consists of a 
directory with the following structure:

```
/<dataset_name>
    <table_name>.csv
    <table_name>.csv
    <table_name>.csv
    metadata.json
```

## Transform the dataset
To create an expanded copy of the `university` dataset, run the following:

```python
from datareactor import DataReactor

reactor = DataReactor()
reactor.transform(
    source="datasets/university",
    destination="/tmp/university"
)
```

This will read the dataset from the `source` directory and generate an expanded
dataset in the `destination` directory which will contain additional columns 
and will have an updated `metadata.json` file which contains information about
those new columns and their lineage.

# What's next?

For more details about **DataReactor** and all its possibilities
and features, please check the [documentation site](
https://data-dev.github.io/DataReactor/).
