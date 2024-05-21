from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.bids.read_sidecar_json import ReadSidecarJSON
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_readsidecarjson_1():
    task = ReadSidecarJSON()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.bids_validate = True
    task.inputs.index_db = Directory.sample(seed=3)
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
