from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.niworkflows.interfaces.reportlets.registration.spatial_normalization_rpt import (
    SpatialNormalizationRPT,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_spatialnormalizationrpt_1():
    task = SpatialNormalizationRPT()
    task.inputs.out_report = "report.svg"
    task.inputs.compress_report = "auto"
    task.inputs.reference_image = Nifti1.sample(seed=3)
    task.inputs.moving_mask = Nifti1.sample(seed=4)
    task.inputs.reference_mask = Nifti1.sample(seed=5)
    task.inputs.lesion_mask = Nifti1.sample(seed=6)
    task.inputs.num_threads = 4
    task.inputs.flavor = "precise"
    task.inputs.template = "MNI152NLin2009cAsym"
    task.inputs.settings = [File.sample(seed=13)]
    task.inputs.explicit_masking = True
    task.inputs.initial_moving_transform = File.sample(seed=17)
    task.inputs.float = False
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
