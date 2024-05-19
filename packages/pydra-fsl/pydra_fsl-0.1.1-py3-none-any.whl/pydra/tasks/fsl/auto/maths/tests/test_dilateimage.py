from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.dilate_image import DilateImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dilateimage_1():
    task = DilateImage()
    task.inputs.kernel_file = File.sample(seed=3)
    task.inputs.in_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
