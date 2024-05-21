from fileformats.generic import File
import logging
import nibabel as nb
import numpy as np
import os
from pathlib import Path
import pydra.mark


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_mask": File}})
def BinaryDilation(in_mask: File, radius: int) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.morphology.binary_dilation import BinaryDilation

    """
    # Open files
    mask_img = nb.load(in_mask)
    maskdata = np.bool_(mask_img.dataobj)

    # Obtain dilated brainmask
    dilated = image_binary_dilation(
        maskdata,
        radius=radius,
    )
    out_file = str((Path(os.getcwd()) / "dilated_mask.nii.gz").absolute())
    out_img = mask_img.__class__(dilated, mask_img.affine, mask_img.header)
    out_img.set_data_dtype("uint8")
    out_img.to_filename(out_file)
    out_mask = out_file

    return out_mask


# Nipype methods converted into functions


def image_binary_dilation(in_mask, radius=2):
    """
    Dilate the input binary mask.

    Parameters
    ----------
    in_mask: :obj:`numpy.ndarray`
        A 3D binary array.
    radius: :obj:`int`, optional
        The radius of the ball-shaped footprint for dilation of the mask.
    """
    from scipy import ndimage as ndi
    from skimage.morphology import ball

    return ndi.binary_dilation(in_mask.astype(bool), ball(radius)).astype(int)
