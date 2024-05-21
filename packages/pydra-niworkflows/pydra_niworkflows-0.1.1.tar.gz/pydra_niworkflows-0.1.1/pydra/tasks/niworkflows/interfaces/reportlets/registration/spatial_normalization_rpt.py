import attrs
from fileformats.application import Dicom
from fileformats.generic import File
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pydra.tasks.ants.auto import registration
from pathlib import Path
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate(
    {
        "return": {
            "out_report": File,
            "reference_image": ty.Union[
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
            "forward_transforms": ty.List[File],
            "reverse_forward_transforms": ty.List[File],
            "reverse_transforms": ty.List[File],
            "forward_invert_flags": list,
            "reverse_forward_invert_flags": list,
            "reverse_invert_flags": list,
            "composite_transform": File,
            "inverse_composite_transform": File,
            "warped_image": ty.Union[
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
            "inverse_warped_image": ty.Union[
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
            "save_state": File,
            "metric_value": float,
            "elapsed_time": float,
        }
    }
)
def SpatialNormalizationRPT(
    out_report: Path,
    compress_report: ty.Any,
    moving_image: ty.Union[
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
    reference_image: ty.Union[
        Nifti1, NiftiGz, Dicom, Bitmap, Tiff, Jpeg, GIPL, MetaImage, Nrrd, NrrdGz, PGM
    ],
    moving_mask: ty.Union[
        Nifti1, NiftiGz, Dicom, Bitmap, Tiff, Jpeg, GIPL, MetaImage, Nrrd, NrrdGz, PGM
    ],
    reference_mask: ty.Union[
        Nifti1, NiftiGz, Dicom, Bitmap, Tiff, Jpeg, GIPL, MetaImage, Nrrd, NrrdGz, PGM
    ],
    lesion_mask: ty.Union[
        Nifti1, NiftiGz, Dicom, Bitmap, Tiff, Jpeg, GIPL, MetaImage, Nrrd, NrrdGz, PGM
    ],
    num_threads: int,
    flavor: ty.Any,
    orientation: ty.Any,
    reference: ty.Any,
    moving: ty.Any,
    template: str,
    settings: ty.List[File],
    template_spec: dict,
    template_resolution: ty.Any,
    explicit_masking: bool,
    initial_moving_transform: File,
    float: bool,
) -> ty.Tuple[
    File,
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
    ty.List[File],
    ty.List[File],
    ty.List[File],
    list,
    list,
    list,
    File,
    File,
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
    File,
    float,
    float,
]:
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.niworkflows.interfaces.reportlets.registration.spatial_normalization_rpt import SpatialNormalizationRPT

    """
    # Get a list of settings files.
    settings_files = _get_settings(moving=moving, settings=settings, flavor=flavor)
    ants_args, _reference_image = _get_ants_args(
        moving_image=moving_image,
        float=float,
        lesion_mask=lesion_mask,
        orientation=orientation,
        flavor=flavor,
        template_resolution=template_resolution,
        reference_mask=reference_mask,
        reference_image=reference_image,
        moving_mask=moving_mask,
        explicit_masking=explicit_masking,
        template_spec=template_spec,
        reference=reference,
        num_threads=num_threads,
        template=template,
        initial_moving_transform=initial_moving_transform,
    )

    if initial_moving_transform is attrs.NOTHING:
        logger.info("Estimating initial transform using AffineInitializer")
        init = AffineInitializer(
            fixed_image=ants_args["fixed_image"],
            moving_image=ants_args["moving_image"],
            num_threads=num_threads,
        )
        init.resource_monitor = False
        init.terminal_output = "allatonce"
        init_result = init.run()
        # Save outputs (if available)
        init_out = _write_outputs(init_result.runtime, ".nipype-init")
        if init_out:
            logger.info(
                "Terminal outputs of initialization saved (%s).",
                ", ".join(init_out),
            )

        ants_args["initial_moving_transform"] = init_result.outputs.out_file

    # For each settings file...
    for ants_settings in settings_files:

        logger.info("Loading settings from file %s.", ants_settings)
        # Configure an ANTs run based on these settings.
        norm = Registration(from_file=ants_settings, **ants_args)
        self.norm.resource_monitor = False
        self.norm.terminal_output = self.terminal_output

        cmd = self.norm.cmdline
        # Print the retry number and command line call to the log.
        logger.info("Retry #%d, commandline: \n%s", self.retry, cmd)
        self.norm.ignore_exception = True
        with open("command.txt", "w") as cmdfile:
            print(cmd + "\n", file=cmdfile)

        # Try running registration.
        interface_result = self.norm.run()

        if interface_result.runtime.returncode != 0:
            logger.warning("Retry #%d failed.", self.retry)
            # Save outputs (if available)
            term_out = _write_outputs(
                interface_result.runtime, ".nipype-%04d" % self.retry
            )
            if term_out:
                logger.warning(
                    "Log of failed retry saved (%s).", ", ".join(term_out)
                )
        else:
            runtime.returncode = 0
            # Note this in the log.
            logger.info(
                "Successful spatial normalization (retry #%d).", self.retry
            )
            # Break out of the retry loop.
            return runtime

        self.retry += 1

    # If all tries fail, raise an error.
    raise RuntimeError(
        "Robust spatial normalization failed after %d retries." % (self.retry - 1)
    )
    try:
        outputs = super(ReportCapableInterface, self)._list_outputs()
    except NotImplementedError:
        outputs = {}
    if self._out_report is not None:
        out_report = self._out_report

    return (
        out_report,
        reference_image,
        forward_transforms,
        reverse_forward_transforms,
        reverse_transforms,
        forward_invert_flags,
        reverse_forward_invert_flags,
        reverse_invert_flags,
        composite_transform,
        inverse_composite_transform,
        warped_image,
        inverse_warped_image,
        save_state,
        metric_value,
        elapsed_time,
    )


# Nipype methods converted into functions


def _get_ants_args(
    moving_image=None,
    float=None,
    lesion_mask=None,
    orientation=None,
    flavor=None,
    template_resolution=None,
    reference_mask=None,
    reference_image=None,
    moving_mask=None,
    explicit_masking=None,
    template_spec=None,
    reference=None,
    num_threads=None,
    template=None,
    initial_moving_transform=None,
):
    _reference_image = attrs.NOTHING
    args = {
        "moving_image": moving_image,
        "num_threads": num_threads,
        "float": float,
        "terminal_output": "file",
        "write_composite_transform": True,
        "initial_moving_transform": initial_moving_transform,
    }

    """
    Moving image handling - The following truth table maps out the intended action
    sequence. Future refactoring may more directly encode this.

    moving_mask and lesion_mask are files
    True = file
    False = None

    | moving_mask | explicit_masking | lesion_mask | action
    |-------------|------------------|-------------|-------------------------------------------
    | True        | True             | True        | Update `moving_image` after applying
    |             |                  |             | mask.
    |             |                  |             | Set `moving_image_masks` applying
    |             |                  |             | `create_cfm` with `global_mask=True`.
    |-------------|------------------|-------------|-------------------------------------------
    | True        | True             | False       | Update `moving_image` after applying
    |             |                  |             | mask.
    |-------------|------------------|-------------|-------------------------------------------
    | True        | False            | True        | Set `moving_image_masks` applying
    |             |                  |             | `create_cfm` with `global_mask=False`
    |-------------|------------------|-------------|-------------------------------------------
    | True        | False            | False       | args['moving_image_masks'] = moving_mask
    |-------------|------------------|-------------|-------------------------------------------
    | False       | *                | True        | Set `moving_image_masks` applying
    |             |                  |             | `create_cfm` with `global_mask=True`
    |-------------|------------------|-------------|-------------------------------------------
    | False       | *                | False       | No action
    """
    # If a moving mask is provided...
    if moving_mask is not attrs.NOTHING:
        # If explicit masking is enabled...
        if explicit_masking:
            # Mask the moving image.
            # Do not use a moving mask during registration.
            args["moving_image"] = mask(
                moving_image,
                moving_mask,
                "moving_masked.nii.gz",
            )

        # If explicit masking is disabled...
        else:
            # Use the moving mask during registration.
            # Do not mask the moving image.
            args["moving_image_masks"] = moving_mask

        # If a lesion mask is also provided...
        if lesion_mask is not attrs.NOTHING:
            # Create a cost function mask with the form:
            # [global mask - lesion mask] (if explicit masking is enabled)
            # [moving mask - lesion mask] (if explicit masking is disabled)
            # Use this as the moving mask.
            args["moving_image_masks"] = create_cfm(
                moving_mask,
                lesion_mask=lesion_mask,
                global_mask=explicit_masking,
            )

    # If no moving mask is provided...
    # But a lesion mask *IS* provided...
    elif lesion_mask is not attrs.NOTHING:
        # Create a cost function mask with the form: [global mask - lesion mask]
        # Use this as the moving mask.
        args["moving_image_masks"] = create_cfm(
            moving_image,
            lesion_mask=lesion_mask,
            global_mask=True,
        )

    """
    Reference image handling - The following truth table maps out the intended action
    sequence. Future refactoring may more directly encode this.

    reference_mask and lesion_mask are files
    True = file
    False = None

    | reference_mask | explicit_masking | lesion_mask | action
    |----------------|------------------|-------------|----------------------------------------
    | True           | True             | True        | Update `fixed_image` after applying
    |                |                  |             | mask.
    |                |                  |             | Set `fixed_image_masks` applying
    |                |                  |             | `create_cfm` with `global_mask=True`.
    |----------------|------------------|-------------|----------------------------------------
    | True           | True             | False       | Update `fixed_image` after applying
    |                |                  |             | mask.
    |----------------|------------------|-------------|----------------------------------------
    | True           | False            | True        | Set `fixed_image_masks` applying
    |                |                  |             | `create_cfm` with `global_mask=False`
    |----------------|------------------|-------------|----------------------------------------
    | True           | False            | False       | args['fixed_image_masks'] = fixed_mask
    |----------------|------------------|-------------|----------------------------------------
    | False          | *                | True        | Set `fixed_image_masks` applying
    |                |                  |             | `create_cfm` with `global_mask=True`
    |----------------|------------------|-------------|----------------------------------------
    | False          | *                | False       | No action
    """
    # If a reference image is provided...
    if reference_image is not attrs.NOTHING:
        # Use the reference image as the fixed image.
        args["fixed_image"] = reference_image
        _reference_image = reference_image

        # If a reference mask is provided...
        if reference_mask is not attrs.NOTHING:
            # If explicit masking is enabled...
            if explicit_masking:
                # Mask the reference image.
                # Do not use a fixed mask during registration.
                args["fixed_image"] = mask(
                    reference_image,
                    reference_mask,
                    "fixed_masked.nii.gz",
                )

                # If a lesion mask is also provided...
                if lesion_mask is not attrs.NOTHING:
                    # Create a cost function mask with the form: [global mask]
                    # Use this as the fixed mask.
                    args["fixed_image_masks"] = create_cfm(
                        reference_mask,
                        lesion_mask=None,
                        global_mask=True,
                    )

            # If a reference mask is provided...
            # But explicit masking is disabled...
            else:
                # Use the reference mask as the fixed mask during registration.
                # Do not mask the fixed image.
                args["fixed_image_masks"] = reference_mask

        # If no reference mask is provided...
        # But a lesion mask *IS* provided ...
        elif lesion_mask is not attrs.NOTHING:
            # Create a cost function mask with the form: [global mask]
            # Use this as the fixed mask
            args["fixed_image_masks"] = create_cfm(
                reference_image, lesion_mask=None, global_mask=True
            )

    # If no reference image is provided, fall back to the default template.
    else:
        from ..utils.misc import get_template_specs

        # Raise an error if the user specifies an unsupported image orientation.
        if orientation == "LAS":
            raise NotImplementedError

        template_spec = template_spec if (template_spec is not attrs.NOTHING) else {}

        default_resolution = {"precise": 1, "fast": 2, "testing": 2}[flavor]

        # Set the template resolution.
        if template_resolution is not attrs.NOTHING:
            logger.warning("The use of ``template_resolution`` is deprecated")
            template_spec["res"] = template_resolution

        template_spec["suffix"] = reference
        template_spec["desc"] = None
        ref_template, template_spec = get_template_specs(
            template,
            template_spec=template_spec,
            default_resolution=default_resolution,
            fallback=True,
        )

        # Set reference image
        _reference_image = ref_template
        if not op.isfile(self._reference_image):
            raise ValueError(
                """\
The registration reference must be an existing file, but path "%s" \
cannot be found."""
                % ref_template
            )

        # Get the template specified by the user.
        ref_mask = get_template(
            template, desc="brain", suffix="mask", **template_spec
        ) or get_template(template, label="brain", suffix="mask", **template_spec)

        # Default is explicit masking disabled
        args["fixed_image"] = ref_template
        # Use the template mask as the fixed mask.
        args["fixed_image_masks"] = str(ref_mask)

        # Overwrite defaults if explicit masking
        if explicit_masking:
            # Mask the template image with the template mask.
            args["fixed_image"] = mask(
                ref_template, str(ref_mask), "fixed_masked.nii.gz"
            )
            # Do not use a fixed mask during registration.
            args.pop("fixed_image_masks", None)

            # If a lesion mask is provided...
            if lesion_mask is not attrs.NOTHING:
                # Create a cost function mask with the form: [global mask]
                # Use this as the fixed mask.
                args["fixed_image_masks"] = create_cfm(
                    str(ref_mask), lesion_mask=None, global_mask=True
                )

    return args, _reference_image


def _get_settings(moving=None, settings=None, flavor=None):
    """
    Return any settings defined by the user, as well as any pre-defined
    settings files that exist for the image modalities to be registered.
    """
    # If user-defined settings exist...
    if settings is not attrs.NOTHING:
        # Note this in the log and return those settings.
        logger.info("User-defined settings, overriding defaults")
        return settings

    # Define a prefix for output files based on the modality of the moving image.
    filestart = "{}-mni_registration_{}_".format(moving.lower(), flavor)

    data_dir = load_data()
    # Get a list of settings files that match the flavor.
    filenames = [
        path.name
        for path in data_dir.iterdir()
        if path.name.startswith(filestart) and path.name.endswith(".json")
    ]
    # Return the settings files.
    return [str(data_dir / f) for f in sorted(filenames)]
