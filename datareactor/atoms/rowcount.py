from datareactor import DerivedColumn
from datareactor.atoms.base import Atom


class RowCountAtom(Atom):
    """Count the number of child rows.

    The `RowCountAtom` generates derived columns which specify the number of
    rows in each of the child columns.
    """

    def derive(self, dataset, table_name):
        """Count the number of rows in each child table.

        This function generates a derived column for each child table which
        contains the number of rows in each group.

        For example, if the target table is users, then it might generate a
        derived column containing the number of rows in the transaction table
        that belongs to each user.

        Args:
            dataset (Dataset): The dataset.
            table_name (str):  The name of the target table.

        Returns:
            (:obj:`list` of :obj:`DerivedColumn`): The derived columns.
        """
        seen = set()

        for foreign_key in dataset.metadata.get_foreign_keys(table_name):
            if foreign_key["table"] == table_name:
                # Skip this relationship if the target table is the child
                continue

            column_name = 'nb_rows_in_%s' % foreign_key["table"]
            if column_name in seen:
                continue
            seen.add(column_name)

            # Count the number of rows for each key.
            child_table = dataset.tables[foreign_key["table"]].copy()
            child_table["_dummy_"] = 1.0
            child_counts = child_table.groupby(foreign_key["field"]).count().iloc[:, 0:1]
            child_counts.columns = [column_name]

            # Merge the counts into the parent table
            parent_table = dataset.tables[table_name]
            parent_table = parent_table.set_index(foreign_key["ref_field"])
            parent_table = parent_table.join(child_counts).reset_index()

            # Set null counts to 0 and specify constraints
            values = parent_table[column_name].fillna(0.0).values

            # Build a derived column object
            derived_column = DerivedColumn()
            derived_column.table_name = table_name
            derived_column.values = values
            derived_column.field = {
                "name": column_name,
                "data_type": "numerical"
            }
            derived_column.constraint = {
                "constraint_type": "lineage",
                "related_fields": [
                    {"table": foreign_key["table"], "field": foreign_key["field"]}
                ],
                "fields_under_consideration": [
                    {"table": foreign_key["ref_table"], "field": column_name}
                ],
                "expression": "datareactor.atoms.RowCountAtom"
            }

            yield derived_column
