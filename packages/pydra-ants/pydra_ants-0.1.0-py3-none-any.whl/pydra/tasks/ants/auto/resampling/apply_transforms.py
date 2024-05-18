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
        "dimension",
        ty.Any,
        {
            "help_string": "This option forces the image to be treated as a specified-dimensional image. If not specified, antsWarp tries to infer the dimensionality from the input image.",
            "argstr": "--dimensionality {dimension}",
        },
    ),
    (
        "input_image_type",
        str,
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
            "output_file_template": '"deformed_moving1.nii"',
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
    (
        "transforms",
        MultiInputObj,
        {
            "help_string": "transform files: will be applied in reverse order. For example, the last specified transform will be applied first.",
            "argstr": "{transforms}",
            "mandatory": True,
        },
    ),
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
ApplyTransforms_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyTransforms_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyTransforms(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.engine.specs import MultiInputObj
    >>> from pydra.tasks.ants.auto.resampling.apply_transforms import ApplyTransforms

    >>> task = ApplyTransforms()
    >>> task.inputs.input_image = "moving1.nii"
    >>> task.inputs.reference_image = "fixed1.nii"
    >>> task.inputs.transforms = "identity"
    >>> task.cmdline
    'antsApplyTransforms --default-value 0 --float 0 --input moving1.nii --interpolation Linear --output moving1_trans.nii --reference-image fixed1.nii --transform identity'


    >>> task = ApplyTransforms()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "moving1.nii"
    >>> task.inputs.output_image = "deformed_moving1.nii"
    >>> task.inputs.reference_image = "fixed1.nii"
    >>> task.inputs.interpolation = "Linear"
    >>> task.inputs.transforms = ["ants_Warp.nii.gz", "trans.mat"]
    >>> task.inputs.invert_transform_flags = [False, True]
    >>> task.inputs.default_value = 0
    >>> task.cmdline
    'antsApplyTransforms --default-value 0 --dimensionality 3 --float 0 --input moving1.nii --interpolation Linear --output deformed_moving1.nii --reference-image fixed1.nii --transform ants_Warp.nii.gz --transform [ trans.mat, 1 ]'


    >>> task = ApplyTransforms()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "moving1.nii"
    >>> task.inputs.output_image = "deformed_moving1.nii"
    >>> task.inputs.reference_image = "fixed1.nii"
    >>> task.inputs.interpolation = "BSpline"
    >>> task.inputs.interpolation_parameters = (5,)
    >>> task.inputs.transforms = ["ants_Warp.nii.gz", "trans.mat"]
    >>> task.inputs.invert_transform_flags = [False, False]
    >>> task.inputs.default_value = 0
    >>> task.cmdline
    'antsApplyTransforms --default-value 0 --dimensionality 3 --float 0 --input moving1.nii --interpolation BSpline[ 5 ] --output deformed_moving1.nii --reference-image fixed1.nii --transform ants_Warp.nii.gz --transform trans.mat'


    >>> task = ApplyTransforms()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "moving1.nii"
    >>> task.inputs.output_image = "deformed_moving1.nii"
    >>> task.inputs.reference_image = "fixed1.nii"
    >>> task.inputs.interpolation = "BSpline"
    >>> task.inputs.interpolation_parameters = (5,)
    >>> task.inputs.transforms = ["identity", "ants_Warp.nii.gz", "trans.mat"]
    >>> task.inputs.default_value = 0
    >>> task.cmdline
    'antsApplyTransforms --default-value 0 --dimensionality 3 --float 0 --input moving1.nii --interpolation BSpline[ 5 ] --output deformed_moving1.nii --reference-image fixed1.nii --transform identity --transform ants_Warp.nii.gz --transform trans.mat'


    """

    input_spec = ApplyTransforms_input_spec
    output_spec = ApplyTransforms_output_spec
    executable = "antsApplyTransforms"
