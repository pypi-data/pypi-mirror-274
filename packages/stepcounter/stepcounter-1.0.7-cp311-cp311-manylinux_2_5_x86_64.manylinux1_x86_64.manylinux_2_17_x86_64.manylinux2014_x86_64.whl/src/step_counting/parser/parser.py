import argparse


MODE_DEFAULT = 'DEFAULT'
MODE_SEQUENCE = 'SEQUENCE'
MODE_DETAIL = 'DETAIL'
MODES = [MODE_DEFAULT, MODE_SEQUENCE, MODE_DETAIL]


def setup_parser() -> argparse.ArgumentParser:
    """
    Sets up argument parser.

    Returns
    -------
    ArgumentParser:  ArgumentParser with added arguments.
    """
    parser = argparse.ArgumentParser(description='Parse command line arguments')
    parser.add_argument('input_file', type=str, help='Input file')
    parser.add_argument(
        '-o', '--output_dir', type=str, help='Output directory', required=False
    )
    parser.add_argument(
        '-m',
        '--mode',
        type=str,
        choices=MODES,
        help='Mode of operation',
        required=False,
    )

    return parser
