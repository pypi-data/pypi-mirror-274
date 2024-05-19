from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.preprocess.susan import SUSAN
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_susan_1():
    task = SUSAN()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.dimension = 3
    task.inputs.use_median = 1
    task.inputs.usans = []
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
