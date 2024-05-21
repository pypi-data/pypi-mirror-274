from fileformats.generic import File
import logging
import nibabel as nb
from pydra.tasks.niworkflows.nipype_ports.utils.filemanip import fname_presuffix
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File, "out_mask": File}})
def Binarize(in_file: File, thresh_low: float) -> ty.Tuple[File, File]:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.nibabel.binarize import Binarize

    """
    img = nb.load(in_file)

    out_file = fname_presuffix(in_file, suffix="_masked", newpath=os.getcwd())
    out_mask = fname_presuffix(in_file, suffix="_mask", newpath=os.getcwd())

    data = img.get_fdata()
    mask = data > thresh_low
    data[~mask] = 0.0
    masked = img.__class__(data, img.affine, img.header)
    masked.to_filename(out_file)

    img.header.set_data_dtype("uint8")
    maskimg = img.__class__(mask.astype("uint8"), img.affine, img.header)
    maskimg.to_filename(out_mask)

    return out_file, out_mask


# Nipype methods converted into functions
