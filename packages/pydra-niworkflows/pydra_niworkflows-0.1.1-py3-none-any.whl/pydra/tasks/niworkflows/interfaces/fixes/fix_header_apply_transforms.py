from fileformats.application import Dicom
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "transforms",
        MultiInputObj,
        {
            "help_string": "transform files: will be applied in reverse order. For example, the last specified transform will be applied first.",
            "argstr": "{transforms}",
            "mandatory": True,
        },
    ),
    (
        "dimension",
        ty.Any,
        {
            "help_string": "This option forces the image to be treated as a specified-dimensional image. If not specified, antsWarp tries to infer the dimensionality from the input image.",
            "argstr": "--dimensionality {dimension}",
        },
    ),
    (
        "input_image_type",
        ty.Any,
        {
            "help_string": "Option specifying the input image type of scalar (default), vector, tensor, or time series.",
            "argstr": "--input-image-type {input_image_type}",
        },
    ),
    (
        "input_image",
        ty.Union[
            ty.List[
                ty.Union[
                    Nifti1,
                    NiftiGz,
                    Dicom,
                    Bitmap,
                    Tiff,
                    Jpeg,
                    GIPL,
                    MetaImage,
                    Nrrd,
                    NrrdGz,
                    PGM,
                ]
            ],
            Nifti1,
            NiftiGz,
            Dicom,
            Bitmap,
            Tiff,
            Jpeg,
            GIPL,
            MetaImage,
            Nrrd,
            NrrdGz,
            PGM,
        ],
        {
            "help_string": "image to apply transformation to (generally a coregistered functional)",
            "argstr": "--input {input_image}",
            "mandatory": True,
        },
    ),
    (
        "output_image",
        str,
        {
            "help_string": "output file name",
            "argstr": "--output {output_image}",
            "output_file_template": "output_image",
        },
    ),
    (
        "out_postfix",
        str,
        "_trans",
        {
            "help_string": "Postfix that is appended to all output files (default = _trans)"
        },
    ),
    (
        "reference_image",
        ty.Union[
            ty.List[
                ty.Union[
                    Nifti1,
                    NiftiGz,
                    Dicom,
                    Bitmap,
                    Tiff,
                    Jpeg,
                    GIPL,
                    MetaImage,
                    Nrrd,
                    NrrdGz,
                    PGM,
                ]
            ],
            Nifti1,
            NiftiGz,
            Dicom,
            Bitmap,
            Tiff,
            Jpeg,
            GIPL,
            MetaImage,
            Nrrd,
            NrrdGz,
            PGM,
        ],
        {
            "help_string": "reference image space that you wish to warp INTO",
            "argstr": "--reference-image {reference_image}",
            "mandatory": True,
        },
    ),
    (
        "interpolation",
        ty.Any,
        "Linear",
        {"help_string": "", "argstr": "{interpolation}"},
    ),
    ("interpolation_parameters", ty.Any, {"help_string": ""}),
    ("invert_transform_flags", MultiInputObj, {"help_string": ""}),
    (
        "default_value",
        float,
        0.0,
        {"help_string": "", "argstr": "--default-value {default_value}"},
    ),
    (
        "print_out_composite_warp_file",
        bool,
        {
            "help_string": "output a composite warp file instead of a transformed image",
            "requires": ["output_image"],
        },
    ),
    (
        "float",
        bool,
        False,
        {
            "help_string": "Use float instead of double for computations.",
            "argstr": "--float {float}",
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
FixHeaderApplyTransforms_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
FixHeaderApplyTransforms_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FixHeaderApplyTransforms(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.engine.specs import MultiInputObj
    >>> from pydra.tasks.niworkflows.interfaces.fixes.fix_header_apply_transforms import FixHeaderApplyTransforms

    """

    input_spec = FixHeaderApplyTransforms_input_spec
    output_spec = FixHeaderApplyTransforms_output_spec
    executable = "antsApplyTransforms"
