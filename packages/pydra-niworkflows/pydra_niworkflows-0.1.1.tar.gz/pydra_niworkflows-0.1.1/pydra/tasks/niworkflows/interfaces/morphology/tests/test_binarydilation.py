from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.morphology.binary_dilation import BinaryDilation
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_binarydilation_1():
    task = BinaryDilation()
    task.inputs.in_mask = File.sample(seed=0)
    task.inputs.radius = 2
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
