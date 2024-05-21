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
def BinarySubtraction(in_base: File, in_subtract: File) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.morphology.binary_subtraction import BinarySubtraction

    """
    # Subtract mask from base
    base_img = nb.load(in_base)
    data = np.bool_(base_img.dataobj)
    data[np.bool_(nb.load(in_subtract).dataobj)] = False

    out_file = str((Path(os.getcwd()) / "subtracted_mask.nii.gz").absolute())
    out_img = base_img.__class__(data, base_img.affine, base_img.header)
    out_img.set_data_dtype("uint8")
    out_img.to_filename(out_file)
    out_mask = out_file

    return out_mask


# Nipype methods converted into functions
