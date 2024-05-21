import logging
from pydra.engine import Workflow
from pydra.tasks.niworkflows.anat.skullstrip import afni_wf


logger = logging.getLogger(__name__)


def test_afni_wf():
    workflow = afni_wf()
    assert isinstance(workflow, Workflow)
