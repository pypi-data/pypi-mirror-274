from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.images.robust_average import RobustAverage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_robustaverage_1():
    task = RobustAverage()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.mc_method = "AFNI"
    task.inputs.nonnegative = True
    task.inputs.two_pass = True
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
