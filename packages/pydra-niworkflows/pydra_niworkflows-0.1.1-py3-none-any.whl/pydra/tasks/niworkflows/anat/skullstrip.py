import attrs
import logging
from pydra.tasks.afni import auto as afni
from pydra.tasks.niworkflows.interfaces.fixes import (
    FixN4BiasFieldCorrection as N4BiasFieldCorrection,
)
from pydra.tasks.niworkflows.interfaces.nibabel import Binarize
from pydra.engine import Workflow
import typing as ty


logger = logging.getLogger(__name__)


def afni_wf(
    in_file=attrs.NOTHING, n4_nthreads=1, name="AFNISkullStripWorkflow", unifize=False
):
    """
    Create a skull-stripping workflow based on AFNI's tools.

    Originally derived from the `codebase of the QAP
    <https://github.com/preprocessed-connectomes-project/quality-assessment-protocol/blob/master/qap/anatomical_preproc.py#L105>`_.
    Now, this workflow includes :abbr:`INU (intensity non-uniformity)` correction
    using the N4 algorithm and (optionally) intensity harmonization using
    ANFI's ``3dUnifize``.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from niworkflows.anat.skullstrip import afni_wf
            wf = afni_wf()

    Parameters
    ----------
    n4_nthreads : int
        number of cpus N4 bias field correction can utilize.
    unifize : bool
        whether AFNI's ``3dUnifize`` should be applied (default: ``False``).
    name : str
        name for the workflow hierarchy of Nipype

    Inputs
    ------
    in_file : str
        input T1w image.

    Outputs
    -------
    bias_corrected : str
        path to the bias corrected input MRI.
    out_file : str
        path to the skull-stripped image.
    out_mask : str
        path to the generated brain mask.
    bias_image : str
        path to the B1 inhomogeneity field.

    """
    workflow = Workflow(
        name=name,
        input_spec={"in_file": ty.Any},
        output_spec={
            "bias_corrected": ty.Any,
            "bias_image": ty.Any,
            "out_file": ty.Any,
            "out_mask": ty.Any,
        },
        in_file=in_file,
    )

    workflow.add(
        N4BiasFieldCorrection(
            copy_header=True,
            dimension=3,
            num_threads=n4_nthreads,
            rescale_intensities=True,
            save_bias=True,
            input_image=workflow.lzin.in_file,
            name="inu_n4",
        )
    )
    workflow.add(afni.SkullStrip(outputtype="NIFTI_GZ", name="sstrip"))
    workflow.add(
        afni.Calc(
            expr="a*step(b)",
            outputtype="NIFTI_GZ",
            in_file_b=workflow.sstrip.lzout.out_file,
            name="sstrip_orig_vol",
        )
    )
    workflow.add(
        Binarize(
            thresh_low=0.0,
            in_file=workflow.sstrip_orig_vol.lzout.out_file,
            name="binarize",
        )
    )
    if unifize:
        # Add two unifize steps, pre- and post- skullstripping.
        workflow.add(afni.Unifize(outputtype="NIFTI_GZ", name="inu_uni_0"))
        workflow.add(afni.Unifize(gm=True, outputtype="NIFTI_GZ", name="inu_uni_1"))
        # fmt: off
        workflow.inu_uni_0.inputs.in_file = workflow.inu_n4.lzout.output_image
        workflow.sstrip.inputs.in_file = workflow.inu_uni_0.lzout.out_file
        workflow.sstrip_orig_vol.inputs.in_file_a = workflow.inu_uni_0.lzout.out_file
        workflow.inu_uni_1.inputs.in_file = workflow.sstrip_orig_vol.lzout.out_file
        workflow.set_output([('out_file', workflow.inu_uni_1.lzout.out_file)])
        workflow.set_output([('bias_corrected', workflow.inu_uni_0.lzout.out_file)])
        # fmt: on
    else:
        # fmt: off
        workflow.sstrip_orig_vol.inputs.in_file_a = workflow.lzin.in_file
        workflow.sstrip.inputs.in_file = workflow.inu_n4.lzout.output_image
        workflow.set_output([('out_file', workflow.sstrip_orig_vol.lzout.out_file)])
        workflow.set_output([('bias_corrected', workflow.inu_n4.lzout.output_image)])
        # fmt: on
    # Remaining connections
    # fmt: off
    workflow.set_output([('out_mask', workflow.binarize.lzout.out_mask)])
    workflow.set_output([('bias_image', workflow.inu_n4.lzout.bias_image)])
    # fmt: on

    return workflow
