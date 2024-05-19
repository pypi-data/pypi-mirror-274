from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.change_data_type import ChangeDataType
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_changedatatype_1():
    task = ChangeDataType()
    task.inputs.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
