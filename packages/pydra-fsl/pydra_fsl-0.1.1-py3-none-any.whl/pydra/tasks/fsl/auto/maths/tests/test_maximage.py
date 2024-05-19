from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.max_image import MaxImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_maximage_1():
    task = MaxImage()
    task.inputs.dimension = "T"
    task.inputs.in_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_maximage_2():
    task = MaxImage()
    task.inputs.in_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
