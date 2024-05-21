import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.fixes.fix_header_apply_transforms import (
    FixHeaderApplyTransforms,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fixheaderapplytransforms_1():
    task = FixHeaderApplyTransforms()
    task.inputs.out_postfix = "_trans"
    task.inputs.interpolation = "Linear"
    task.inputs.default_value = 0.0
    task.inputs.float = False
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
