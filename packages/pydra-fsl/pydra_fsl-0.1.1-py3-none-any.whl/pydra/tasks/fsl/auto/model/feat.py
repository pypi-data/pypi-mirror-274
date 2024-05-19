from fileformats.generic import Directory, File
import logging
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "fsf_file",
        File,
        {
            "help_string": "File specifying the feat design spec file",
            "argstr": "{fsf_file}",
            "mandatory": True,
            "position": 0,
        },
    )
]
FEAT_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("feat_dir", Directory, {})]
FEAT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FEAT(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.fsl.auto.model.feat import FEAT

    """

    input_spec = FEAT_input_spec
    output_spec = FEAT_output_spec
    executable = "feat"
