"""Top-level package for DataReactor."""

import logging

from datareactor.dataset import Dataset, DerivedColumn
from datareactor.reactor import DataReactor

__author__ = 'MIT Data To AI Lab'
__email__ = 'dailabmit@gmail.com'
__version__ = '0.1.0.dev0'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


__all__ = ['Dataset', 'DataReactor', 'DerivedColumn']
