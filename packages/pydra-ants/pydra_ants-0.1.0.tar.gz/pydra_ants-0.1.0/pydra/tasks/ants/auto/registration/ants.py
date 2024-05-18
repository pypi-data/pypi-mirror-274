from fileformats.application import Dicom
from fileformats.generic import File
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "dimension",
        ty.Any,
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "{dimension}",
            "position": 1,
        },
    ),
    (
        "fixed_image",
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
        {"help_string": "image to which the moving image is warped", "mandatory": True},
    ),
    (
        "moving_image",
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
        {
            "help_string": "image to apply transformation to (generally a coregisteredfunctional)",
            "argstr": "{moving_image}",
            "mandatory": True,
        },
    ),
    ("metric", list, {"help_string": "", "mandatory": True}),
    (
        "metric_weight",
        list,
        {
            "help_string": "the metric weight(s) for each stage. The weights must sum to 1 per stage.",
            "mandatory": True,
            "requires": ["metric"],
        },
    ),
    (
        "radius",
        list,
        {
            "help_string": "radius of the region (i.e. number of layers around a voxel/pixel) that is used for computing cross correlation",
            "mandatory": True,
            "requires": ["metric"],
        },
    ),
    (
        "output_transform_prefix",
        str,
        {
            "help_string": "",
            "argstr": "--output-naming {output_transform_prefix}",
            "mandatory": True,
        },
    ),
    (
        "transformation_model",
        ty.Any,
        {"help_string": "", "argstr": "{transformation_model}", "mandatory": True},
    ),
    (
        "gradient_step_length",
        float,
        {"help_string": "", "requires": ["transformation_model"]},
    ),
    (
        "number_of_time_steps",
        int,
        {"help_string": "", "requires": ["gradient_step_length"]},
    ),
    ("delta_time", float, {"help_string": "", "requires": ["number_of_time_steps"]}),
    ("symmetry_type", float, {"help_string": "", "requires": ["delta_time"]}),
    (
        "use_histogram_matching",
        bool,
        True,
        {"help_string": "", "argstr": "{use_histogram_matching}"},
    ),
    (
        "number_of_iterations",
        list,
        {
            "help_string": "",
            "argstr": "--number-of-iterations {number_of_iterations}",
            "sep": "x",
        },
    ),
    (
        "smoothing_sigmas",
        list,
        {
            "help_string": "",
            "argstr": "--gaussian-smoothing-sigmas {smoothing_sigmas}",
            "sep": "x",
        },
    ),
    (
        "subsampling_factors",
        list,
        {
            "help_string": "",
            "argstr": "--subsampling-factors {subsampling_factors}",
            "sep": "x",
        },
    ),
    (
        "affine_gradient_descent_option",
        list,
        {"help_string": "", "argstr": "{affine_gradient_descent_option}"},
    ),
    (
        "mi_option",
        list,
        {"help_string": "", "argstr": "--MI-option {mi_option}", "sep": "x"},
    ),
    ("regularization", ty.Any, {"help_string": "", "argstr": "{regularization}"}),
    (
        "regularization_gradient_field_sigma",
        float,
        {"help_string": "", "requires": ["regularization"]},
    ),
    (
        "regularization_deformation_field_sigma",
        float,
        {"help_string": "", "requires": ["regularization"]},
    ),
    (
        "number_of_affine_iterations",
        list,
        {
            "help_string": "",
            "argstr": "--number-of-affine-iterations {number_of_affine_iterations}",
            "sep": "x",
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ANTS_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("affine_transform", File, {"help_string": "Affine transform file"}),
    ("warp_transform", File, {"help_string": "Warping deformation field"}),
    (
        "inverse_warp_transform",
        File,
        {"help_string": "Inverse warping deformation field"},
    ),
    ("metaheader", File, {"help_string": "VTK metaheader .mhd file"}),
    ("metaheader_raw", File, {"help_string": "VTK metaheader .raw file"}),
]
ANTS_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ANTS(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.registration.ants import ANTS

    >>> task = ANTS()
    >>> task.inputs.dimension = 3
    >>> task.inputs.fixed_image = ["T1.nii"]
    >>> task.inputs.moving_image = ["resting.nii"]
    >>> task.inputs.metric = ["CC"]
    >>> task.inputs.metric_weight = [1.0]
    >>> task.inputs.radius = [5]
    >>> task.inputs.output_transform_prefix = "MY"
    >>> task.inputs.transformation_model = "SyN"
    >>> task.inputs.gradient_step_length = 0.25
    >>> task.inputs.use_histogram_matching = True
    >>> task.inputs.number_of_iterations = [50, 35, 15]
    >>> task.inputs.mi_option = [32, 16000]
    >>> task.inputs.regularization = "Gauss"
    >>> task.inputs.regularization_gradient_field_sigma = 3
    >>> task.inputs.regularization_deformation_field_sigma = 0
    >>> task.inputs.number_of_affine_iterations = [10000,10000,10000,10000,10000]
    >>> task.cmdline
    'ANTS 3 --MI-option 32x16000 --image-metric CC[ T1.nii, resting.nii, 1, 5 ] --number-of-affine-iterations 10000x10000x10000x10000x10000 --number-of-iterations 50x35x15 --output-naming MY --regularization Gauss[3.0,0.0] --transformation-model SyN[0.25] --use-Histogram-Matching 1'


    """

    input_spec = ANTS_input_spec
    output_spec = ANTS_output_spec
    executable = "ANTS"
