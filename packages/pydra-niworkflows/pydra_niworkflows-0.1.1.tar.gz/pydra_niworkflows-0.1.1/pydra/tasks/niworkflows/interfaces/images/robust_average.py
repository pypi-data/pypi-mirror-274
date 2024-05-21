import attrs
from fileformats.generic import File
from functools import partial
import logging
import nibabel as nb
from pydra.tasks.niworkflows.nipype_ports.utils.filemanip import fname_presuffix
import numpy as np
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate(
    {
        "return": {
            "out_file": File,
            "out_volumes": File,
            "out_drift": list,
            "out_hmc": ty.List[File],
            "out_hmc_volumes": ty.List[File],
        }
    }
)
def RobustAverage(
    in_file: File,
    t_mask: list,
    mc_method: ty.Any,
    nonnegative: bool,
    num_threads: int,
    two_pass: bool,
) -> ty.Tuple[File, File, list, ty.List[File], ty.List[File]]:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.images.robust_average import RobustAverage

    """
    img = nb.load(in_file)

    # If reference is 3D, return it directly
    if img.dataobj.ndim == 3:
        out_file = in_file
        out_volumes = in_file
        out_drift = [1.0]
        return runtime

    fname = partial(fname_presuffix, in_file, newpath=os.getcwd())

    # Slicing may induce inconsistencies with shape-dependent values in extensions.
    # For now, remove all. If this turns out to be a mistake, we can select extensions
    # that don't break pipeline stages.
    img.header.extensions.clear()
    img = nb.squeeze_image(img)

    # If reference was 4D, but single-volume - write out squeezed and return.
    if img.dataobj.ndim == 3:
        out_file = fname(suffix="_squeezed")
        img.to_filename(out_file)
        out_volumes = in_file
        out_drift = [1.0]
        return runtime

    img_len = img.shape[3]
    t_mask = t_mask if (t_mask is not attrs.NOTHING) else [True] * img_len

    if len(t_mask) != img_len:
        raise ValueError(
            f"Image length ({img_len} timepoints) unmatched by mask ({len(t_mask)})"
        )

    n_volumes = sum(t_mask)
    if n_volumes < 1:
        raise ValueError("At least one volume should be selected for slicing")

    out_file = fname(suffix="_average")
    out_volumes = fname(suffix="_sliced")

    sliced = nb.concat_images(i for i, t in zip(nb.four_to_three(img), t_mask) if t)

    data = sliced.get_fdata(dtype="float32")
    # Data can come with outliers showing very high numbers - preemptively prune
    data = np.clip(
        data,
        a_min=0.0 if nonnegative else np.percentile(data, 0.2),
        a_max=np.percentile(data, 99.8),
    )

    gs_drift = np.mean(data, axis=(0, 1, 2))
    gs_drift /= gs_drift.max()
    out_drift = [float(i) for i in gs_drift]

    data /= gs_drift
    data = np.clip(
        data,
        a_min=0.0 if nonnegative else data.min(),
        a_max=data.max(),
    )
    sliced.__class__(data, sliced.affine, sliced.header).to_filename(out_volumes)

    if n_volumes == 1:
        nb.squeeze_image(sliced).to_filename(out_file)
        out_drift = [1.0]
        return runtime

    if mc_method == "AFNI":
        from nipype.interfaces.afni import Volreg

        volreg = Volreg(
            in_file=out_volumes,
            interp="Fourier",
            args="-twopass" if two_pass else "",
            zpad=4,
            outputtype="NIFTI_GZ",
        )
        if num_threads is not attrs.NOTHING:
            volreg.inputs.num_threads = num_threads

        res = volreg.run()
        out_hmc = res.outputs.oned_matrix_save

    elif mc_method == "FSL":
        from nipype.interfaces.fsl import MCFLIRT

        res = MCFLIRT(
            in_file=out_volumes,
            ref_vol=0,
            interpolation="sinc",
        ).run()
        out_hmc = res.outputs.mat_file

    if mc_method:
        out_hmc_volumes = res.outputs.out_file
        data = nb.load(res.outputs.out_file).get_fdata(dtype="float32")

    data = np.clip(
        data,
        a_min=0.0 if nonnegative else data.min(),
        a_max=data.max(),
    )

    sliced.__class__(np.median(data, axis=3), sliced.affine, sliced.header).to_filename(
        out_file
    )

    return out_file, out_volumes, out_drift, out_hmc, out_hmc_volumes


# Nipype methods converted into functions
