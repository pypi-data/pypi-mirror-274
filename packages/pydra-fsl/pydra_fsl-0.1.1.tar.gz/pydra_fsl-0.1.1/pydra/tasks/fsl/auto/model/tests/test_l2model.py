import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.l2_model import L2Model
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_l2model_1():
    task = L2Model()
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
