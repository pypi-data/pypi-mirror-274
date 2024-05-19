from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fix.classifier import Classifier
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_classifier_1():
    task = Classifier()
    task.inputs.mel_ica = Directory.sample(seed=0)
    task.inputs.trained_wts_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
