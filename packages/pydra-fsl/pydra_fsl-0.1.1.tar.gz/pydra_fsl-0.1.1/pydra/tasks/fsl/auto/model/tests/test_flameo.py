from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1, NiftiGz
from fileformats.medimage_fsl import Con
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.flameo import FLAMEO
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_flameo_1():
    task = FLAMEO()
    task.inputs.cope_file = NiftiGz.sample(seed=0)
    task.inputs.var_cope_file = NiftiGz.sample(seed=1)
    task.inputs.dof_var_cope_file = File.sample(seed=2)
    task.inputs.mask_file = Nifti1.sample(seed=3)
    task.inputs.design_file = TextMatrix.sample(seed=4)
    task.inputs.t_con_file = Con.sample(seed=5)
    task.inputs.f_con_file = File.sample(seed=6)
    task.inputs.cov_split_file = TextMatrix.sample(seed=7)
    task.inputs.log_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_flameo_2():
    task = FLAMEO()
    task.inputs.cope_file = NiftiGz.sample(seed=0)
    task.inputs.var_cope_file = NiftiGz.sample(seed=1)
    task.inputs.mask_file = Nifti1.sample(seed=3)
    task.inputs.design_file = TextMatrix.sample(seed=4)
    task.inputs.t_con_file = Con.sample(seed=5)
    task.inputs.cov_split_file = TextMatrix.sample(seed=7)
    task.inputs.run_mode = "fe"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
