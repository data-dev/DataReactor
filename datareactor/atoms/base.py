import logging

from datareactor.dataset import Dataset, DerivedColumn

logger = logging.getLogger(__name__)


class Atom():
    """Generate derived columns for a dataset.

    Each `Atom` is responsible for generating one or more derived columns for
    the target table.
    """

    def transform(self, dataset):
        """Generate derived columns for the dataset.

        The `transform` function takes in a dataset and returns a sequence of
        derived columns.

        Args:
            dataset (Dataset): The dataset.

        Returns:
            (:obj:`list` of :obj:`DerivedColumn`): The derived columns.
        """
        derived_columns = []
        assert isinstance(dataset, Dataset)
        for table_name in dataset.metadata.get_table_names():
            logger.info("Generating columns in table %s using %s." % (
                table_name,
                self.__class__.__name__
            ))
            for derived_column in self.derive(dataset, table_name):
                assert isinstance(derived_column, DerivedColumn)
                derived_columns.append(derived_column)
        return derived_columns

    def derive(self, dataset, table_name):
        """Generate derived columns for the specified table.

        The `derive` function takes in a dataset and the name of the target
        column. It returns a list of derived columns which can be concatenated
        to the target table.

        Args:
            dataset (Dataset): The dataset.
            table_name (str):  The name of the target table.

        Returns:
            (:obj:`list` of :obj:`DerivedColumn`): The derived columns.
        """
        raise NotImplementedError()
