from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.isotropic_smooth import IsotropicSmooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_isotropicsmooth_1():
    task = IsotropicSmooth()
    task.inputs.in_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
