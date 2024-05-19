from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fix.cleaner import Cleaner
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_cleaner_1():
    task = Cleaner()
    task.inputs.artifacts_list_file = File.sample(seed=0)
    task.inputs.highpass = 100
    task.inputs.confound_file = File.sample(seed=4)
    task.inputs.confound_file_1 = File.sample(seed=5)
    task.inputs.confound_file_2 = File.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
