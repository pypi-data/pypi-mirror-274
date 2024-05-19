from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        Nifti1,
        {
            "help_string": "input filename",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_base_name",
        str,
        {"help_string": "outputs prefix", "argstr": "{out_base_name}", "position": 1},
    ),
]
Slice_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_files", ty.List[File], {})]
Slice_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Slice(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.fsl.auto.utils.slice import Slice

    >>> task = Slice()
    >>> task.inputs.in_file = Nifti1.mock("functional.nii")
    >>> task.inputs.out_base_name = "sl"
    >>> task.cmdline
    'fslslice functional.nii sl'


    """

    input_spec = Slice_input_spec
    output_spec = Slice_output_spec
    executable = "fslslice"
