import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.level_1_design import Level1Design
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_level1design_1():
    task = Level1Design()
    task.inputs.orthogonalization = {}
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
