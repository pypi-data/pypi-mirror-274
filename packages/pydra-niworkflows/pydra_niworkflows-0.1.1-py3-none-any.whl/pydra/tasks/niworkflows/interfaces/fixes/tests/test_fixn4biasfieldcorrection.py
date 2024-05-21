import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.fixes.fix_n4_bias_field_correction import (
    FixN4BiasFieldCorrection,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fixn4biasfieldcorrection_1():
    task = FixN4BiasFieldCorrection()
    task.inputs.dimension = 3
    task.inputs.rescale_intensities = False
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
