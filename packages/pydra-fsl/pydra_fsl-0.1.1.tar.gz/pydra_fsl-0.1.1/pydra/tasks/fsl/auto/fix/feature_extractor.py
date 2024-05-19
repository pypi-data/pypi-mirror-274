from fileformats.generic import Directory
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "mel_ica",
        Path,
        {
            "help_string": "Melodic output directory or directories",
            "argstr": "{mel_ica}",
            "copyfile": False,
            "position": -1,
        },
    )
]
FeatureExtractor_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("mel_ica", Directory, {"help_string": "Melodic output directory or directories"})
]
FeatureExtractor_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FeatureExtractor(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from pydra.tasks.fsl.auto.fix.feature_extractor import FeatureExtractor

    """

    input_spec = FeatureExtractor_input_spec
    output_spec = FeatureExtractor_output_spec
    executable = "fix -f"
