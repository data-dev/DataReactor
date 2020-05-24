"""DataReactor CLI.

Usage:
    datareactor <path_to_input> <path_to_output> [--quiet]

Options:
    -h --help            Show this screen.
    --quiet              Whether to print logs.
"""
import logging

from docopt import docopt

from datareactor import DataReactor


def main():
    args = docopt(__doc__)
    if not args["--quiet"]:
        logger = logging.getLogger("datareactor")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(levelname)s:%(name)s.%(filename)s — %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    reactor = DataReactor()
    reactor.transform(
        source=args['<path_to_input>'],
        destination=args['<path_to_output>']
    )


if __name__ == '__main__':
    main()
