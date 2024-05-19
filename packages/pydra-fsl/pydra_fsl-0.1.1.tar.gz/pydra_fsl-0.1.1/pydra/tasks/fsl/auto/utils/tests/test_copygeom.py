from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.copy_geom import CopyGeom
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_copygeom_1():
    task = CopyGeom()
    task.inputs.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
