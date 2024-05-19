from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.slice import Slice
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_slice_1():
    task = Slice()
    task.inputs.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_slice_2():
    task = Slice()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_base_name = "sl"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
