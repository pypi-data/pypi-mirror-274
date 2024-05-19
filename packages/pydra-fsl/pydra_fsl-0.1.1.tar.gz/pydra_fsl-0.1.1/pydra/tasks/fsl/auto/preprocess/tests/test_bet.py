from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.preprocess.bet import BET
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_bet_1():
    task = BET()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.t2_guided = File.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bet_2():
    task = BET()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.out_file = "brain_anat.nii"
    task.inputs.frac = 0.7
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
