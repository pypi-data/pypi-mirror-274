from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.nibabel.intensity_clip import IntensityClip
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_intensityclip_1():
    task = IntensityClip()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.p_min = 35.0
    task.inputs.p_max = 99.98
    task.inputs.nonnegative = True
    task.inputs.dtype = "int16"
    task.inputs.invert = False
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
