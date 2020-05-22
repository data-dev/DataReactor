from datareactor import DerivedColumn
from datareactor.atoms.base import Atom


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
                (lambda x: x.std(), "std")
            ]:
                # Count the number of rows for each key.
                child_table = dataset.tables[fk["table"]].copy()
                if len(child_table.columns) <= 1:
                    continue
                child_counts = op(child_table.groupby(fk["field"]))
                old_column_names = list(child_counts.columns)
                child_counts.columns = ["%s(%s)" % (op_name, col_name)
                                        for col_name in old_column_names]

                # Merge the counts into the parent table
                parent_table = dataset.tables[fk["ref_table"]]
                parent_table = parent_table.set_index(fk["ref_field"])
                parent_table = parent_table.join(child_counts).reset_index()

                for old_name, col_name in zip(old_column_names, child_counts.columns):
                    if parent_table[col_name].dtype.kind != "f":
                        continue
                    if col_name in seen:
                        continue
                    seen.add(col_name)

                    values = parent_table[col_name].fillna(0.0).values

                    column = DerivedColumn()
                    column.table_name = table_name
                    column.values = values
                    column.field = {
                        "name": col_name,
                        "data_type": "numerical"
                    }
                    column.constraint = {
                        "constraint_type": "lineage",
                        "related_fields": [
                            {"table": fk["table"], "field": old_name}
                        ],
                        "fields_under_consideration": [
                            {"table": fk["ref_table"], "field": col_name}
                        ],
                        "expression": "datareactor.atoms.AggregationAtom"
                    }
                    yield column
