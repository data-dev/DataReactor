import numpy as np

from datareactor.atoms.base import Atom
from datareactor.dataset import DerivedColumn


class AddNumericalAtom(Atom):
    """Add a random set of columns.

    The `AddNumericalAtom` generates a derived column which contains the sum
    of a random set of numerical columns in the same table.
    """

    def derive(self, dataset, table_name):
        """Add a column containing random values.
        """
        df = dataset.tables[table_name].select_dtypes("number")
        if len(df.columns) > 1:
            cols = np.random.choice(df.columns, size=5)
            df = df[list(set(cols))].copy().fillna(0.0)
        new_col = df.sum(axis=1)

        derived_column = DerivedColumn()
        derived_column.table_name = table_name
        derived_column.values = new_col.values
        derived_column.field = {
            "name": "add_numerical",
            "data_type": "numerical"
        }
        derived_column.constraint = {
            "constraint_type": "lineage",
            "related_fields": [
                {"table": table_name, "field": col_name} for col_name in df.columns
            ],
            "fields_under_consideration": [
                {"table": table_name, "field": "add_numerical"}
            ]
        }
        yield derived_column
