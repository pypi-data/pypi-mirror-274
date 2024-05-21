from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.nibabel.apply_mask import ApplyMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applymask_1():
    task = ApplyMask()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.in_mask = File.sample(seed=1)
    task.inputs.threshold = 0.5
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
