from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.temporal_filter import TemporalFilter
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_temporalfilter_1():
    task = TemporalFilter()
    task.inputs.lowpass_sigma = -1
    task.inputs.highpass_sigma = -1
    task.inputs.in_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
