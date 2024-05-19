import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.fix.feature_extractor import FeatureExtractor
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_featureextractor_1():
    task = FeatureExtractor()
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
