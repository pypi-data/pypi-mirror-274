from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.preprocess.fast import FAST
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fast_1():
    task = FAST()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.init_transform = File.sample(seed=10)
    task.inputs.other_priors = [File.sample(seed=11)]
    task.inputs.manual_seg = File.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fast_2():
    task = FAST()
    task.inputs.in_files = [Nifti1.sample(seed=0)]
    task.inputs.out_basename = "fast_"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
