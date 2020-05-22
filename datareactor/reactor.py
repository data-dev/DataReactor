from datareactor.atoms import Atom
from datareactor.dataset import Dataset
from datareactor.sieve import Sieve


class DataReactor():
    """Transform datasets by generating derived columns.

    The `DataReactor` class provides methods for transforming relational
    datasets by creating derived columns with known lineage.

    Attributes:
        atoms: A list of `Atom` objects to apply to generate columns.
        sieve: The sieve to use to filter columns.
    """

    def __init__(self, atoms=None, sieve=None):
        """Initialize a `DataReactor`.

        Args:
            atoms: A list of `Atom` objects to apply.
        """
        if not atoms:
            atoms = [atom() for atom in Atom.__subclasses__()]
        self.atoms = atoms
        self.sieve = sieve if sieve else Sieve()

    def transform(self, source, destination):
        """Read, transform, and write the dataset.

        This function reads the dataset from the source location, generates
        derived columns using the atoms, filters the derived columns using a
        sieve, and writes the modified dataset to the destination location.

        Args:
            source (str): The dataset path to read from.
            destination (str): The dataset path to write to.
        """
        dataset = Dataset(source)

        derived_columns = []
        for atom in self.atoms:
            derived_columns.extend(atom.transform(dataset))
        derived_columns = self.sieve.filter(dataset, derived_columns)

        dataset.add_columns(derived_columns)
        dataset.export(destination)
