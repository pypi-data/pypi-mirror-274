from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.percentile_image import PercentileImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_percentileimage_1():
    task = PercentileImage()
    task.inputs.dimension = "T"
    task.inputs.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_percentileimage_2():
    task = PercentileImage()
    task.inputs.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
