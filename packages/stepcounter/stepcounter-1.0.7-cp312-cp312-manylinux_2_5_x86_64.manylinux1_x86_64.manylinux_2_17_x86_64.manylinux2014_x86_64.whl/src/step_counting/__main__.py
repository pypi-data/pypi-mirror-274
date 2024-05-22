from types import ModuleType

from .setup_recording import setup_recording, RecodingActivated
from .profiler.profiler import output_profile
from .parser.parser import setup_parser
from .utils.module import import_from_path, insert_module_to_path


def main() -> None:
    """
    Main function of the script.

    Script flow:
        - Parse arguments
        - Insert input file to path
        - Import module from input path
        - Setup recording
        - Evaluate function of imported module
        - Output profile and overall score

    Returns
    -------
    None
    """
    parser = setup_parser()
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_dir
    mode = args.mode

    insert_module_to_path(input_file)

    eval_module: ModuleType = import_from_path(input_file)
    if not hasattr(eval_module, 'main'):
        raise AttributeError(
            f'Given module with path: {input_file} does not contain a main function!'
        )

    recorder, tracked_modules = setup_recording(eval_module, mode, set())

    with RecodingActivated():
        eval_module.main()

    output_profile(recorder, output_file, tracked_modules, mode)


if __name__ == '__main__':
    main()
