from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.warp_utils import WarpUtils
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warputils_1():
    task = WarpUtils()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warputils_2():
    task = WarpUtils()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    task.inputs.out_format = "spline"
    task.inputs.warp_resolution = (10, 10, 10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
