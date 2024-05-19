from fileformats.datascience import TextMatrix
from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.convert_xfm import ConvertXFM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_convertxfm_1():
    task = ConvertXFM()
    task.inputs.in_file = TextMatrix.sample(seed=0)
    task.inputs.in_file2 = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_convertxfm_2():
    task = ConvertXFM()
    task.inputs.in_file = TextMatrix.sample(seed=0)
    task.inputs.invert_xfm = True
    task.inputs.out_file = "flirt_inv.mat"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
