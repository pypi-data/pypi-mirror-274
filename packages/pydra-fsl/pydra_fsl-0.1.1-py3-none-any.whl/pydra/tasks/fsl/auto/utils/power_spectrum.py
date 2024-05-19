from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "input 4D file to estimate the power spectrum",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "name of output 4D file for power spectrum",
            "argstr": "{out_file}",
            "position": 1,
            "output_file_template": "out_file",
        },
    ),
]
PowerSpectrum_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
PowerSpectrum_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PowerSpectrum(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.auto.utils.power_spectrum import PowerSpectrum

    """

    input_spec = PowerSpectrum_input_spec
    output_spec = PowerSpectrum_output_spec
    executable = "fslpspec"
