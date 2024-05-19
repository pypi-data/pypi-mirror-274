from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.medimage_fsl import Con
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.randomise import Randomise
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_randomise_1():
    task = Randomise()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.base_name = "randomise"
    task.inputs.design_mat = TextMatrix.sample(seed=2)
    task.inputs.tcon = Con.sample(seed=3)
    task.inputs.fcon = File.sample(seed=4)
    task.inputs.mask = Nifti1.sample(seed=5)
    task.inputs.x_block_labels = File.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_randomise_2():
    task = Randomise()
    task.inputs.in_file = Nifti1.sample(seed=0)
    task.inputs.design_mat = TextMatrix.sample(seed=2)
    task.inputs.tcon = Con.sample(seed=3)
    task.inputs.mask = Nifti1.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
