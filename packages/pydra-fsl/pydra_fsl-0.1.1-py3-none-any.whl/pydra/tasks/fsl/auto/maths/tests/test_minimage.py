from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.min_image import MinImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_minimage_1():
    task = MinImage()
    task.inputs.dimension = "T"
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
