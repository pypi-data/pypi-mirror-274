from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.warp_points import WarpPoints
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warppoints_1():
    task = WarpPoints()
    task.inputs.src_file = Nifti1.sample(seed=0)
    task.inputs.dest_file = Nifti1.sample(seed=1)
    task.inputs.in_coords = TextFile.sample(seed=2)
    task.inputs.xfm_file = File.sample(seed=3)
    task.inputs.warp_file = Nifti1.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warppoints_2():
    task = WarpPoints()
    task.inputs.src_file = Nifti1.sample(seed=0)
    task.inputs.dest_file = Nifti1.sample(seed=1)
    task.inputs.in_coords = TextFile.sample(seed=2)
    task.inputs.warp_file = Nifti1.sample(seed=4)
    task.inputs.coord_mm = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
