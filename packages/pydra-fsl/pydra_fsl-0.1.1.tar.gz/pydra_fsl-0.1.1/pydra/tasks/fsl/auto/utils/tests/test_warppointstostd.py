from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.warp_points_to_std import WarpPointsToStd
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warppointstostd_1():
    task = WarpPointsToStd()
    task.inputs.img_file = Nifti1.sample(seed=0)
    task.inputs.std_file = Nifti1.sample(seed=1)
    task.inputs.premat_file = File.sample(seed=2)
    task.inputs.in_coords = TextFile.sample(seed=3)
    task.inputs.xfm_file = File.sample(seed=4)
    task.inputs.warp_file = Nifti1.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warppointstostd_2():
    task = WarpPointsToStd()
    task.inputs.img_file = Nifti1.sample(seed=0)
    task.inputs.std_file = Nifti1.sample(seed=1)
    task.inputs.in_coords = TextFile.sample(seed=3)
    task.inputs.warp_file = Nifti1.sample(seed=5)
    task.inputs.coord_mm = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
