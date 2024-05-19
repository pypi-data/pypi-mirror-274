from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.smooth_estimate import SmoothEstimate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smoothestimate_1():
    task = SmoothEstimate()
    task.inputs.mask_file = Nifti1.sample(seed=1)
    task.inputs.residual_fit_file = File.sample(seed=2)
    task.inputs.zstat_file = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smoothestimate_2():
    task = SmoothEstimate()
    task.inputs.mask_file = Nifti1.sample(seed=1)
    task.inputs.zstat_file = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
