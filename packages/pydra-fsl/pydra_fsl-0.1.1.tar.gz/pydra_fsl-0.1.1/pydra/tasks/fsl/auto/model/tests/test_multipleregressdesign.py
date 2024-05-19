import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.model.multiple_regress_design import MultipleRegressDesign
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_multipleregressdesign_1():
    task = MultipleRegressDesign()
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
