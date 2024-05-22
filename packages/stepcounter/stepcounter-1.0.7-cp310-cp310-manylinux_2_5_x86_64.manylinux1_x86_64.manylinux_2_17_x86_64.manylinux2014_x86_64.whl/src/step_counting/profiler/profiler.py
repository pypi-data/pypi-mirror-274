import os
from types import ModuleType
from typing import Any

from ..parser.parser import MODE_DETAIL, MODE_SEQUENCE

from step_counting.decorator.records.record_classes import (
    Counter,
    SequenceCallRecorder,
    DetailCallRecorder,
    Recorder,
)


class Profile_detail:
    module_profiles: dict[ModuleType, str] = dict()
    evaluation: int = 0


def create_module_profile(
    module_file: str, module_data: dict[int, dict[Any, Counter]]
) -> str:
    """
    Creates a profile for given module. Information about operations on each
    line are added as commentary at the end of the line.

    Parameters
    ----------
    module_file (str): path to the file where the module is defined
    module_data (dict): data collected for given module

    Returns
    -------
    str: Profile of the program
    """
    lines = []
    with open(module_file, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            lines.append(f'{line_number}: {line[0:-1]}')

            lines.append((90 - len(str(line_number)) - len(line)) * ' ')
            for record, counter in module_data.get(line_number, {}).items():
                module, class_, func = record
                class_name = class_.__name__ + '.' if class_ else ''
                lines.append(
                    f' # {module.__name__}.{class_name}{func}: No of calls: {counter.get_count_total()}, Total eval: {counter.get_evaluation_total()}\n'
                )

                lines.append(91 * ' ')

            lines[-1] = '\n'

    return ''.join(lines)


def create_profile_sequence(recorder: SequenceCallRecorder) -> str:
    """
    Creates a profile for sequence mode recording.

    Parameters
    ----------
    recorder (SequenceCallRecorder): recorder for sequence recording

    Returns
    -------
    str: sequence calls in text form
    """
    sequence_profile = []
    for record in recorder.get_data():
        class_ = record[1]
        class_name = ' ' + class_.__name__ if class_ else ''
        sequence_profile.append(f'{record[0].__name__}{class_name} {record[2]}\n')

    return ''.join(sequence_profile)


def create_profile_detail(
    modules: set[ModuleType],
    recorder: DetailCallRecorder,
) -> Profile_detail:
    """
    Creates a profile for all modules.

    Parameters
    ----------
    modules (set): set of modules to profile
    recorder (DetailCallRecorder): recorder for detail recording

    Returns
    -------
    Profile_detail: structure with information for each module profile
    and total evaluation
    """
    profile = Profile_detail()
    profile.evaluation = recorder.evaluate_data()
    data = recorder.get_data()

    for module in modules:
        module_data = data.get(module, {})

        assert module.__file__
        profile.module_profiles[module] = create_module_profile(
            module.__file__, module_data
        )

    return profile


def output_to_stdout(profile: Profile_detail) -> None:
    """
    Outputs all given module profiles to stdout

    Parameters
    ----------
    module_profiles (dict): profiles for each module

    Returns
    -------
    None
    """
    for module, module_profile in profile.module_profiles.items():
        print(module.__name__)
        print(module_profile)
    print(f'SCORE: {profile.evaluation}')


def profile_to_file(profile: str, output_file: str) -> None:
    """
    Outputs profile to file.

    Parameters
    ----------
    profile (str): profile of a module
    output_file (str): output file to which the profile will be written

    Returns
    -------
    None
    """
    with open(output_file, 'w') as file:
        file.write(profile)


def output_to_dir(profile: Profile_detail, output_dir: str) -> None:
    """
    Outputs all profiles to directory, each to separate file.

    Parameters
    ----------
    module_profiles (dict): profiles for each module
    output_dir (str): path to the dir to which profile files will be writen

    Returns
    -------
    None
    """
    for module, module_profile in profile.module_profiles.items():
        filepath = os.path.join(output_dir, module.__name__)
        profile_to_file(module_profile, filepath)
    profile_to_file(
        f'Score: {profile.evaluation}', os.path.join(output_dir, 'evaluation')
    )


def output_profile_detail(profile: Profile_detail, output_dir: str) -> None:
    """
    Determines if profiles should be written to stdout or directory.

    Parameters
    ----------
    module_profiles (dict): profiles for each module
    output_dir (str): path to the dir to which profile files will be writen

    Returns
    -------
    None
    """
    if output_dir is None:
        output_to_stdout(profile)
    else:
        output_to_dir(profile, output_dir)


def output_profile(
    recorder: Recorder,
    output_dir: str,
    tracked_modules: set[ModuleType],
    mode: str,
) -> None:
    """
    Outputs the profile to specified directory.
    If the direcroty is not specified, outputs to stdout.

    Parameters
    ----------
    recorder (Recorder): simple/sequence/detail recorder
    module_profiles (dict): profiles for each module
    output_dir (str): path to the dir to which profile files will be writen
    mode: mode of recording

    Returns
    -------
    None
    """
    evaluation = recorder.evaluate_data()
    if mode == MODE_SEQUENCE:
        score_text = f'No of operations: {evaluation}'
        sequence_profile = create_profile_sequence(recorder)
        if output_dir is None:
            print(sequence_profile)
            print(score_text)
        else:
            output_file = os.path.join(output_dir, 'sequence-evaluation')
            profile_to_file(score_text, output_file)
    elif mode == MODE_DETAIL:
        profile = create_profile_detail(tracked_modules, recorder)
        output_profile_detail(profile, output_dir)
    else:
        score_text = f'Score: {evaluation}'
        if output_dir is None:
            print(score_text)
        else:
            output_file = os.path.join(output_dir, 'evaluation')
            profile_to_file(score_text, output_file)
