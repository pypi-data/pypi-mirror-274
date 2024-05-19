from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.unary_maths import UnaryMaths
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_unarymaths_1():
    task = UnaryMaths()
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
