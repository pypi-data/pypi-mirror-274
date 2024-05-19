from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.median_image import MedianImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_medianimage_1():
    task = MedianImage()
    task.inputs.dimension = "T"
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
