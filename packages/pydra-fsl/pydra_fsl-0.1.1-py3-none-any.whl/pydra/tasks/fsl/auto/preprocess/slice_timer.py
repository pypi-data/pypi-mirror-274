from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "in_file",
        File,
        {
            "help_string": "filename of input timeseries",
            "argstr": "--in={in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {"help_string": "filename of output timeseries", "argstr": "--out={out_file}"},
    ),
    (
        "index_dir",
        bool,
        {"help_string": "slice indexing from top to bottom", "argstr": "--down"},
    ),
    (
        "time_repetition",
        float,
        {
            "help_string": "Specify TR of data - default is 3s",
            "argstr": "--repeat={time_repetition}",
        },
    ),
    (
        "slice_direction",
        ty.Any,
        {
            "help_string": "direction of slice acquisition (x=1, y=2, z=3) - default is z",
            "argstr": "--direction={slice_direction}",
        },
    ),
    (
        "interleaved",
        bool,
        {"help_string": "use interleaved acquisition", "argstr": "--odd"},
    ),
    (
        "custom_timings",
        File,
        {
            "help_string": "slice timings, in fractions of TR, range 0:1 (default is 0.5 = no shift)",
            "argstr": "--tcustom={custom_timings}",
        },
    ),
    (
        "global_shift",
        float,
        {
            "help_string": "shift in fraction of TR, range 0:1 (default is 0.5 = no shift)",
            "argstr": "--tglobal",
        },
    ),
    (
        "custom_order",
        File,
        {
            "help_string": "filename of single-column custom interleave order file (first slice is referred to as 1 not 0)",
            "argstr": "--ocustom={custom_order}",
        },
    ),
]
SliceTimer_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("slice_time_corrected_file", File, {"help_string": "slice time corrected file"})
]
SliceTimer_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SliceTimer(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.auto.preprocess.slice_timer import SliceTimer

    """

    input_spec = SliceTimer_input_spec
    output_spec = SliceTimer_output_spec
    executable = "slicetimer"
