from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.nibabel.binarize import Binarize
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_binarize_1():
    task = Binarize()
    task.inputs.in_file = File.sample(seed=0)
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
