import logging

import pandas as pd

from datareactor import DerivedColumn
from datareactor.atoms.base import Atom

logger = logging.getLogger(__name__)


class AggregationAtom(Atom):
    """Apply aggregation functions to child rows.

    The `AggregationAtom` generates derived columns which are the resultt of
    applying aggregation functions to groups of child rows.
    """

    def derive(self, dataset, table_name):
        """Apply pandas aggregation functions to groups of rows.

        Returns:
            (:obj:`list` of :obj:`DerivedColumn`): The derived columns.
        """
        seen = set()

        for fk in dataset.metadata.get_foreign_keys(table_name):
            if fk["table"] == table_name:
                # Skip this relationship if the target table is the child
                continue

            for op, op_name in [
                (lambda x: x.sum(), "sum"),
                (lambda x: x.max(), "max"),
                (lambda x: x.min(), "min"),
            ]:
                logger.info("Applying aggregator %s to foreign key %s -> %s." % (
                    op_name, fk["ref_table"], fk["table"]
                ))

                # Count the number of rows for each key.
                child_table = dataset.tables[fk["table"]].copy()
                if len(child_table.columns) <= 1:
                    continue
                child_table = child_table.set_index(fk["field"]).select_dtypes("number")
                child_counts = op(child_table.groupby(fk["field"]))
                column_names = list(child_counts.columns)
                child_counts.columns = ["%s(%s)" % (op_name, col) for col in column_names]

                # Merge the counts into the parent table
                parent_table = dataset.tables[fk["ref_table"]].copy()
                parent_table = pd.merge(
                    parent_table.reset_index(),
                    child_counts.reset_index(),
                    how='left',
                    left_on=fk["ref_field"],
                    right_on=fk["field"]
                ).set_index(fk["ref_field"])

                for column_name, derived_name in zip(column_names, child_counts.columns):
                    if parent_table[derived_name].dtype.kind != "f":
                        continue
                    if derived_name in seen:
                        continue
                    seen.add(derived_name)

                    values = parent_table[derived_name].fillna(0.0).values

                    column = DerivedColumn()
                    column.table_name = table_name
                    column.values = values
                    column.field = {
                        "name": derived_name,
                        "data_type": "numerical"
                    }
                    column.constraint = {
                        "constraint_type": "lineage",
                        "related_fields": [
                            {"table": fk["table"], "field": column_name}
                        ],
                        "fields_under_consideration": [
                            {"table": fk["ref_table"], "field": derived_name}
                        ],
                        "expression": "datareactor.atoms.AggregationAtom"
                    }
                    yield column
