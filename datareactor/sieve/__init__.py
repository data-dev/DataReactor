import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Sieve():
    """
    The `Sieve` class filters out derived columns that don't make sense.
    """

    def filter(self, dataset, columns):
        """
        The `filter` function takes in a dataset and a list of derived columns;
        it returns a subset of the derived columns after removing any derived
        columns which don't make sense - i.e. all constant values, redundant
        with another column, etc.

        Args:
            dataset (Dataset): The dataset.
            columns (:obj:`list` of :obj:`DerivedColumn`): The derived columns.

        Returns:
            A list of derived columns.
        """
        value_hashes = dict()
        filtered_columns = []
        for column in columns:
            if np.mean(pd.isna(column.values)) > 0.5:
                logger.info(
                    "Skipping %s.%s, it is NaN more than half the time.",
                    column.table_name,
                    column.field["name"]
                )
                continue

            values = tuple([value for value in column.values])
            if len(set(values)) == 1:
                logger.info(
                    "Skipping %s.%s, it has a constant value of %s.",
                    column.table_name,
                    column.field["name"],
                    values[0]
                )
                continue

            value_hash = hash(values)
            if value_hash in value_hashes:
                logger.info(
                    "Skipping %s.%s, it is identical to %s.%s.",
                    column.table_name,
                    column.field["name"],
                    value_hashes[value_hash].table_name,
                    value_hashes[value_hash].field["name"]
                )
                continue
            value_hashes[value_hash] = column

            filtered_columns.append(column)

        return filtered_columns
