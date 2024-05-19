from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    ("in_file", File, {"help_string": "", "argstr": "{in_file}", "mandatory": True}),
    (
        "out_file",
        Path,
        {"help_string": "", "argstr": "{out_file}", "output_file_template": "out_file"},
    ),
]
Reorient2Std_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Reorient2Std_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Reorient2Std(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.auto.utils.reorient_2_std import Reorient2Std

    """

    input_spec = Reorient2Std_input_spec
    output_spec = Reorient2Std_output_spec
    executable = "fslreorient2std"
