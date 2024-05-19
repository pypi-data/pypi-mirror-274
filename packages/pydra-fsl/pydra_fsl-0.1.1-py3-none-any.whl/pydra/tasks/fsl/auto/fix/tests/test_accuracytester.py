from fileformats.generic import File
from fileformats.medimage_fsl import MelodicIca
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fix.accuracy_tester import AccuracyTester
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_accuracytester_1():
    task = AccuracyTester()
    task.inputs.mel_icas = [MelodicIca.sample(seed=0)]
    task.inputs.trained_wts_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
