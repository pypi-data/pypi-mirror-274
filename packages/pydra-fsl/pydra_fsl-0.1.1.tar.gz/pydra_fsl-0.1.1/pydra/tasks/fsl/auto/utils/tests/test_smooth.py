from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.smooth import Smooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smooth_1():
    task = Smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smooth_2():
    task = Smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.sigma = 8.0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smooth_3():
    task = Smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.fwhm = 8.0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smooth_4():
    task = Smooth()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
