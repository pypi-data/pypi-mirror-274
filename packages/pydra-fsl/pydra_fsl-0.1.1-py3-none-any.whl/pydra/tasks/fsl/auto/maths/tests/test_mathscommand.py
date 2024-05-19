from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.maths_command import MathsCommand
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mathscommand_1():
    task = MathsCommand()
    task.inputs.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
