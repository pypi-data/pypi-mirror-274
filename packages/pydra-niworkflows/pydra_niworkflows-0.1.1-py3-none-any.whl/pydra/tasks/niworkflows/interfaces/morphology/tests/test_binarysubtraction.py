from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.morphology.binary_subtraction import (
    BinarySubtraction,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_binarysubtraction_1():
    task = BinarySubtraction()
    task.inputs.in_base = File.sample(seed=0)
    task.inputs.in_subtract = File.sample(seed=1)
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
