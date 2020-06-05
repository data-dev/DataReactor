import logging
import os

import pandas as pd

from metad import MetaData

logger = logging.getLogger(__name__)


def _read_csv_dtypes(table_meta):
    """Get the dtypes specification that needs to be passed to read_csv."""
    dtypes = dict()
    for field in table_meta['fields']:
        if 'data_type' not in field:
            continue
        field_type = field['data_type']
        if field_type == 'categorical':
            dtypes[field['name']] = str
        elif field_type == 'id' and field.get('data_subtype', 'integer') == 'string':
            dtypes[field['name']] = str
    return dtypes


def _parse_dtypes(data, table_meta):
    """Convert the data columns to the right dtype after loading the CSV."""
    for field in table_meta['fields']:
        if 'data_type' not in field:
            continue
        field_type = field['data_type']
        if field_type == 'datetime':
            datetime_format = field.get('format')
            data[field['name']] = pd.to_datetime(
                data[field['name']], format=datetime_format, exact=False)
        elif field_type == 'numerical' and field.get('data_subtype') == 'integer':
            data[field['name']] = data[field['name']].dropna().astype(int)
        elif field_type == 'id' and field.get('data_subtype', 'integer') == 'integer':
            data[field['name']] = data[field['name']].dropna().astype(int)
    return data


class DerivedColumn():
    """Derived column with known lineage.

    The `DerivedColumn` represents a derived column which belongs to the
    specified table.

    Attributes:
        table_name (str): The name of the table the column will belong to.
        values (list): A series of values which can be added to the table.
        field (dict): A field object which specifies the name and data type.
        constraint (:obj:`dict`, None): An optional constraint object.
    """

    table_name = None
    values = None
    field = None
    constraint = None


class Dataset():
    """Read and write `metad` datasets.

    The `Dataset` object provides methods for reading datasets, adding derived
    columns, and writing datasets.

    Attributes:
        path_to_dataset: The path to the dataset files.
        metadata: The metad.MetaData object.
        tables: A dictionary mapping table names to dataframes.
    """

    def __init__(self, path_to_dataset):
        """Read the dataset from disk.

        Args:
            path_to_dataset (str): The path to the dataset.
        """
        self.path_to_dataset = os.path.expanduser(path_to_dataset)

        path_to_metadata = os.path.join(self.path_to_dataset, "metadata.json")
        self.metadata = MetaData.from_json(path_to_metadata)

        self.tables = {}
        for table_name in self.metadata.get_table_names():
            path_to_csv = os.path.join(self.path_to_dataset, "%s.csv" % table_name)

            table_metadata = self.metadata.get_table(table_name)
            dtypes = _read_csv_dtypes(table_metadata)
            self.tables[table_name] = pd.read_csv(path_to_csv, dtype=dtypes)
            _parse_dtypes(self.tables[table_name], table_metadata)

            logger.info("Loaded table %s (%s rows, %s cols)" % (
                table_name,
                len(self.tables[table_name]),
                len(self.tables[table_name].columns)
            ))

    def export(self, path_to_dataset):
        """Write the dataset to disk.

        This writes the dataset to the target directory. It creates the tables
        as CSV files and writes the metadata as a JSON file.

        Args:
            path_to_dataset (str): The path to the dataset.
        """
        path_to_dataset = os.path.expanduser(path_to_dataset)
        os.makedirs(path_to_dataset, exist_ok=True)
        self.metadata.to_json(os.path.join(path_to_dataset, "metadata.json"))
        for table_name, dataframe in self.tables.items():
            path_to_csv = os.path.join(path_to_dataset, "%s.csv" % table_name)
            dataframe.to_csv(path_to_csv, index=False)
            logger.info("Exported table %s (%s rows, %s cols)" % (
                table_name,
                len(self.tables[table_name]),
                len(self.tables[table_name].columns)
            ))

    def add_columns(self, columns):
        """Add the derived columns to the dataset.

        This modifies the tables and metadata in-place and adds the specified
        derived columns.

        Args:
            columns (:obj:`list` of :obj:`DerivedColumn`): The derived columns.
        """
        for col in columns:
            if col.field["name"] in self.tables[col.table_name].columns:
                raise ValueError("Column aleady exists!")
            self.tables[col.table_name][col.field["name"]] = col.values
            self.metadata.add_field(col.table_name, col.field)
            if col.constraint:
                self.metadata.add_constraint(col.constraint)
