from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.split import Split
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_split_1():
    task = Split()
    task.inputs.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
