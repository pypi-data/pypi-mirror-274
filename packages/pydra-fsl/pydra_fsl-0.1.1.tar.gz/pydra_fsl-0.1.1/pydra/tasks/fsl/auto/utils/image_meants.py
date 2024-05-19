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
            "help_string": "input file for computing the average timeseries",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "name of output text matrix",
            "argstr": "-o {out_file}",
            "output_file_template": "out_file",
        },
    ),
    ("mask", File, {"help_string": "input 3D mask", "argstr": "-m {mask}"}),
    (
        "spatial_coord",
        list,
        {
            "help_string": "<x y z>  requested spatial coordinate (instead of mask)",
            "argstr": "-c {spatial_coord}",
        },
    ),
    (
        "use_mm",
        bool,
        {
            "help_string": "use mm instead of voxel coordinates (for -c option)",
            "argstr": "--usemm",
        },
    ),
    (
        "show_all",
        bool,
        {
            "help_string": "show all voxel time series (within mask) instead of averaging",
            "argstr": "--showall",
        },
    ),
    (
        "eig",
        bool,
        {
            "help_string": "calculate Eigenvariate(s) instead of mean (output will have 0 mean)",
            "argstr": "--eig",
        },
    ),
    (
        "order",
        int,
        1,
        {"help_string": "select number of Eigenvariates", "argstr": "--order={order}"},
    ),
    (
        "nobin",
        bool,
        {
            "help_string": "do not binarise the mask for calculation of Eigenvariates",
            "argstr": "--no_bin",
        },
    ),
    (
        "transpose",
        bool,
        {
            "help_string": "output results in transpose format (one row per voxel/mean)",
            "argstr": "--transpose",
        },
    ),
]
ImageMeants_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ImageMeants_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ImageMeants(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.auto.utils.image_meants import ImageMeants

    """

    input_spec = ImageMeants_input_spec
    output_spec = ImageMeants_output_spec
    executable = "fslmeants"
