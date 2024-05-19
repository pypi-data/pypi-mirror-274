from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.contrast_mgr import ContrastMgr
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_contrastmgr_1():
    task = ContrastMgr()
    task.inputs.tcon_file = File.sample(seed=0)
    task.inputs.fcon_file = File.sample(seed=1)
    task.inputs.param_estimates = [File.sample(seed=2)]
    task.inputs.corrections = File.sample(seed=3)
    task.inputs.dof_file = File.sample(seed=4)
    task.inputs.sigmasquareds = File.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
