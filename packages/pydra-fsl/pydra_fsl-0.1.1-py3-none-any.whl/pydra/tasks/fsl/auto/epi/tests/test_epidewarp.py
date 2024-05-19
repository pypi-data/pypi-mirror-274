from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.epi.epi_de_warp import EPIDeWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_epidewarp_1():
    task = EPIDeWarp()
    task.inputs.mag_file = Nifti1.sample(seed=0)
    task.inputs.dph_file = Nifti1.sample(seed=1)
    task.inputs.exf_file = File.sample(seed=2)
    task.inputs.epi_file = Nifti1.sample(seed=3)
    task.inputs.tediff = 2.46
    task.inputs.esp = 0.58
    task.inputs.sigma = 2
    task.inputs.nocleanup = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_epidewarp_2():
    task = EPIDeWarp()
    task.inputs.mag_file = Nifti1.sample(seed=0)
    task.inputs.dph_file = Nifti1.sample(seed=1)
    task.inputs.epi_file = Nifti1.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
