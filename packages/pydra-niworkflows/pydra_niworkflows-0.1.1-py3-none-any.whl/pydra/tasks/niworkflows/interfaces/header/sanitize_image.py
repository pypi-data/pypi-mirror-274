from fileformats.generic import File
import logging
import nibabel as nb
from pydra.tasks.niworkflows.nipype_ports.utils.filemanip import fname_presuffix
import numpy as np
import os
import pydra.mark
from textwrap import indent
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File, "out_report": File}})
def SanitizeImage(
    in_file: File, n_volumes_to_discard: int, max_32bit: bool
) -> ty.Tuple[File, File]:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.niworkflows.interfaces.header.sanitize_image import SanitizeImage

    """
    img = nb.load(in_file)
    out_report = os.path.join(os.getcwd(), "report.html")

    # Retrieve xform codes
    sform_code = int(img.header._structarr["sform_code"])
    qform_code = int(img.header._structarr["qform_code"])

    # Check qform is valid
    valid_qform = False
    try:
        img.get_qform()
        valid_qform = True
    except ValueError:
        pass

    # Matching affines
    matching_affines = valid_qform and np.allclose(img.get_qform(), img.get_sform())

    save_file = False
    warning_txt = ""

    # Both match, qform valid (implicit with match), codes okay -> do nothing, empty report
    if matching_affines and qform_code > 0 and sform_code > 0:
        out_file = in_file
        open(out_report, "w").close()

    # Row 2:
    elif valid_qform and qform_code > 0:
        img.set_sform(img.get_qform(), qform_code)
        save_file = True
        warning_txt = "Note on orientation: sform matrix set"
        description = """\
<p class="elem-desc">The sform has been copied from qform.</p>
"""
    # Rows 3-4:
    # Note: if qform is not valid, matching_affines is False
    elif sform_code > 0 and (not matching_affines or qform_code == 0):
        img.set_qform(img.get_sform(), sform_code)
        save_file = True
        warning_txt = "Note on orientation: qform matrix overwritten"
        description = """\
<p class="elem-desc">The qform has been copied from sform.</p>
"""
        if not valid_qform and qform_code > 0:
            warning_txt = "WARNING - Invalid qform information"
            description = """\
<p class="elem-desc">
The qform matrix found in the file header is invalid.
The qform has been copied from sform.
Checking the original qform information from the data produced
by the scanner is advised.
</p>
"""
    # Rows 5-6:
    else:
        affine = img.affine
        img.set_sform(affine, nb.nifti1.xform_codes["scanner"])
        img.set_qform(affine, nb.nifti1.xform_codes["scanner"])
        save_file = True
        warning_txt = "WARNING - Missing orientation information"
        description = """\
<p class="elem-desc">
Orientation information could not be retrieved from the image header.
The qform and sform matrices have been set to a default, LAS-oriented affine.
Analyses of this dataset MAY BE INVALID.
</p>
"""

    if (
        max_32bit and np.dtype(img.get_data_dtype()).itemsize > 4
    ) or n_volumes_to_discard:
        # force float32 only if 64 bit dtype is detected
        if max_32bit and np.dtype(img.get_data_dtype()).itemsize > 4:
            in_data = img.get_fdata(dtype=np.float32)
        else:
            in_data = img.dataobj

        img = nb.Nifti1Image(
            in_data[:, :, :, n_volumes_to_discard:],
            img.affine,
            img.header,
        )
        save_file = True

    if len(img.header.extensions) != 0:
        img.header.extensions.clear()
        save_file = True

    # Store new file
    if save_file:
        out_fname = fname_presuffix(in_file, suffix="_valid", newpath=os.getcwd())
        out_file = out_fname
        img.to_filename(out_fname)

    if warning_txt:
        snippet = '<h3 class="elem-title">%s</h3>\n%s\n' % (
            warning_txt,
            description,
        )
        with open(out_report, "w") as fobj:
            fobj.write(indent(snippet, "\t" * 3))

    out_report = out_report

    return out_file, out_report


# Nipype methods converted into functions
