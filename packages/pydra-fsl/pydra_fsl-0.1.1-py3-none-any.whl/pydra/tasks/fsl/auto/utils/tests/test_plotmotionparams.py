import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.plot_motion_params import PlotMotionParams
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_plotmotionparams_1():
    task = PlotMotionParams()
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
