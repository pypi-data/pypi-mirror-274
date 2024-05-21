from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.header.sanitize_image import SanitizeImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sanitizeimage_1():
    task = SanitizeImage()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.n_volumes_to_discard = 0
    task.inputs.max_32bit = False
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
