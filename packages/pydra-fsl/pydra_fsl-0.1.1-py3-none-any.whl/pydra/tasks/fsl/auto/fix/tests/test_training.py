from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fix.training import Training
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_training_1():
    task = Training()
    task.inputs.mel_icas = [File.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
