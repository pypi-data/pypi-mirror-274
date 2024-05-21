from fileformats.generic import File
import logging
import nibabel as nb
import numpy as np
import os
from pathlib import Path
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def IntensityClip(
    in_file: File,
    p_min: float,
    p_max: float,
    nonnegative: bool,
    dtype: ty.Any,
    invert: bool,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.nibabel.intensity_clip import IntensityClip

    """
    out_file = _advanced_clip(
        in_file,
        p_min=p_min,
        p_max=p_max,
        nonnegative=nonnegative,
        dtype=dtype,
        invert=invert,
        newpath=os.getcwd(),
    )

    return out_file


# Nipype methods converted into functions


def _advanced_clip(
    in_file,
    p_min=35,
    p_max=99.98,
    nonnegative=True,
    dtype="int16",
    invert=False,
    newpath=None,
):
    """
    Remove outliers at both ends of the intensity distribution and fit into a given dtype.

    This interface tries to emulate ANTs workflows' massaging that truncate images into
    the 0-255 range, and applies percentiles for clipping images.
    For image registration, normalizing the intensity into a compact range (e.g., uint8)
    is generally advised.

    To more robustly determine the clipping thresholds, data are removed of spikes
    with a median filter.
    Once the thresholds are calculated, the denoised data are thrown away and the thresholds
    are applied on the original image.

    """
    from pathlib import Path
    import nibabel as nb
    import numpy as np
    from scipy import ndimage
    from skimage.morphology import ball

    out_file = (Path(newpath or "") / "clipped.nii.gz").absolute()
    # Load data
    img = nb.squeeze_image(nb.load(in_file))
    if len(img.shape) != 3:
        raise RuntimeError(f"<{in_file}> is not a 3D file.")
    data = img.get_fdata(dtype="float32")
    # Calculate stats on denoised version, to preempt outliers from biasing
    denoised = ndimage.median_filter(data, footprint=ball(3))
    a_min = np.percentile(denoised[denoised > 0] if nonnegative else denoised, p_min)
    a_max = np.percentile(denoised[denoised > 0] if nonnegative else denoised, p_max)
    # Clip and cast
    data = np.clip(data, a_min=a_min, a_max=a_max)
    data -= data.min()
    data /= data.max()
    if invert:
        data = 1.0 - data
    if dtype in ("uint8", "int16"):
        data = np.round(255 * data).astype(dtype)
    hdr = img.header.copy()
    hdr.set_data_dtype(dtype)
    img.__class__(data, img.affine, hdr).to_filename(out_file)
    return str(out_file)
