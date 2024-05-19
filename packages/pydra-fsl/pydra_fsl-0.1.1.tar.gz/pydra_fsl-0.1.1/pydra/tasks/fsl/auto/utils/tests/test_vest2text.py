from fileformats.datascience import TextMatrix
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.vest_2_text import Vest2Text
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_vest2text_1():
    task = Vest2Text()
    task.inputs.in_file = TextMatrix.sample(seed=0)
    task.inputs.out_file = "design.txt"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_vest2text_2():
    task = Vest2Text()
    task.inputs.in_file = TextMatrix.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
