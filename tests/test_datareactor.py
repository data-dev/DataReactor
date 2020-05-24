import tempfile
import unittest
from glob import glob

from parameterized import parameterized

from datareactor import DataReactor


class TestDataReactor(unittest.TestCase):

    @parameterized.expand(glob("datasets/**/"))
    def test_datasets(self, path_to_example):
        reactor = DataReactor()
        with tempfile.TemporaryDirectory() as path_to_output:
            reactor.transform(
                path_to_example,
                path_to_output
            )
