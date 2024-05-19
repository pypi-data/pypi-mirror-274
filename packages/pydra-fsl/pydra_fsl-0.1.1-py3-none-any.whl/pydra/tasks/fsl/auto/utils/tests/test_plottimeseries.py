from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.plot_time_series import PlotTimeSeries
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_plottimeseries_1():
    task = PlotTimeSeries()
    task.inputs.legend_file = File.sample(seed=5)
    task.inputs.x_units = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
