from fileformats.generic import File
from fileformats.medimage import Bval, Bvec, Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.dti.dti_fit import DTIFit
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dtifit_1():
    task = DTIFit()
    task.inputs.dwi = Nifti1.sample(seed=0)
    task.inputs.base_name = "dtifit_"
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.bvecs = Bvec.sample(seed=3)
    task.inputs.bvals = Bval.sample(seed=4)
    task.inputs.cni = File.sample(seed=13)
    task.inputs.gradnonlin = File.sample(seed=15)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_dtifit_2():
    task = DTIFit()
    task.inputs.dwi = Nifti1.sample(seed=0)
    task.inputs.base_name = "TP"
    task.inputs.mask = Nifti1.sample(seed=2)
    task.inputs.bvecs = Bvec.sample(seed=3)
    task.inputs.bvals = Bval.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
