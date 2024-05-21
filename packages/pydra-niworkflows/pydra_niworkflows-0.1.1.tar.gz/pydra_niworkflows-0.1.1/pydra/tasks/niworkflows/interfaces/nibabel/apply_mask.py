from fileformats.generic import File
import logging
import nibabel as nb
from pydra.tasks.niworkflows.nipype_ports.utils.filemanip import fname_presuffix
import numpy as np
import os
import pydra.mark


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def ApplyMask(in_file: File, in_mask: File, threshold: float) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.nibabel.apply_mask import ApplyMask

    """
    img = nb.load(in_file)
    msknii = nb.load(in_mask)
    msk = msknii.get_fdata() > threshold

    out_file = fname_presuffix(in_file, suffix="_masked", newpath=os.getcwd())

    if img.dataobj.shape[:3] != msk.shape:
        raise ValueError("Image and mask sizes do not match.")

    if not np.allclose(img.affine, msknii.affine):
        raise ValueError("Image and mask affines are not similar enough.")

    if img.dataobj.ndim == msk.ndim + 1:
        msk = msk[..., np.newaxis]

    masked = img.__class__(img.dataobj * msk, None, img.header)
    masked.to_filename(out_file)

    return out_file


# Nipype methods converted into functions
