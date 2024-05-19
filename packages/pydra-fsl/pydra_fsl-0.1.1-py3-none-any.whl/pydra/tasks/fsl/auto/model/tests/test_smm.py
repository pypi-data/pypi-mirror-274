from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.smm import SMM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smm_1():
    task = SMM()
    task.inputs.spatial_data_file = File.sample(seed=0)
    task.inputs.mask = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
