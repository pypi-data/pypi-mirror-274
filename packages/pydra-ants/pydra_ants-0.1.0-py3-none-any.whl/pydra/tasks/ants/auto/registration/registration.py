from fileformats.application import Dicom
from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
from pydra.engine.specs import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


def elapsed_time_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["elapsed_time"]


def metric_value_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["metric_value"]


input_fields = [
    (
        "dimension",
        ty.Any,
        3,
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "--dimensionality {dimension}",
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
        {
            "help_string": "Image to which the moving_image should be transformed(usually a structural image)",
            "mandatory": True,
        },
    ),
    (
        "fixed_image_mask",
        File,
        {
            "help_string": "Mask used to limit metric sampling region of the fixed imagein all stages",
            "argstr": "{fixed_image_mask}",
            "xor": ["fixed_image_masks"],
        },
    ),
    (
        "fixed_image_masks",
        MultiInputObj,
        {
            "help_string": 'Masks used to limit metric sampling region of the fixed image, defined per registration stage(Use "NULL" to omit a mask at a given stage)',
            "xor": ["fixed_image_mask"],
        },
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
            "help_string": "Image that will be registered to the space of fixed_image. This is theimage on which the transformations will be applied to",
            "mandatory": True,
        },
    ),
    (
        "moving_image_mask",
        File,
        {
            "help_string": "mask used to limit metric sampling region of the moving imagein all stages",
            "requires": ["fixed_image_mask"],
            "xor": ["moving_image_masks"],
        },
    ),
    (
        "moving_image_masks",
        MultiInputObj,
        {
            "help_string": 'Masks used to limit metric sampling region of the moving image, defined per registration stage(Use "NULL" to omit a mask at a given stage)',
            "xor": ["moving_image_mask"],
        },
    ),
    (
        "save_state",
        Path,
        {
            "help_string": "Filename for saving the internal restorable state of the registration",
            "argstr": "--save-state {save_state}",
        },
    ),
    (
        "restore_state",
        TextMatrix,
        {
            "help_string": "Filename for restoring the internal restorable state of the registration",
            "argstr": "--restore-state {restore_state}",
        },
    ),
    (
        "initial_moving_transform",
        ty.List[TextMatrix],
        {
            "help_string": "A transform or a list of transforms that should be applied before the registration begins. Note that, when a list is given, the transformations are applied in reverse order.",
            "argstr": "{initial_moving_transform}",
            "xor": ["initial_moving_transform_com"],
        },
    ),
    (
        "invert_initial_moving_transform",
        MultiInputObj,
        {
            "help_string": "One boolean or a list of booleans that indicatewhether the inverse(s) of the transform(s) definedin initial_moving_transform should be used.",
            "requires": ["initial_moving_transform"],
            "xor": ["initial_moving_transform_com"],
        },
    ),
    (
        "initial_moving_transform_com",
        ty.Any,
        {
            "help_string": "Align the moving_image and fixed_image before registration using the geometric center of the images (=0), the image intensities (=1), or the origin of the images (=2).",
            "argstr": "{initial_moving_transform_com}",
            "xor": ["initial_moving_transform"],
        },
    ),
    ("metric_item_trait", ty.Any, {"help_string": ""}),
    ("metric_stage_trait", ty.Any, {"help_string": ""}),
    (
        "metric",
        list,
        {
            "help_string": "the metric(s) to use for each stage. Note that multiple metrics per stage are not supported in ANTS 1.9.1 and earlier.",
            "mandatory": True,
        },
    ),
    ("metric_weight_item_trait", float, 1.0, {"help_string": ""}),
    ("metric_weight_stage_trait", ty.Any, {"help_string": ""}),
    (
        "metric_weight",
        list,
        {
            "help_string": "the metric weight(s) for each stage. The weights must sum to 1 per stage.",
            "mandatory": True,
            "requires": ["metric"],
        },
    ),
    ("radius_bins_item_trait", int, 5, {"help_string": ""}),
    ("radius_bins_stage_trait", ty.Any, {"help_string": ""}),
    (
        "radius_or_number_of_bins",
        list,
        [5],
        {
            "help_string": "the number of bins in each stage for the MI and Mattes metric, the radius for other metrics",
            "requires": ["metric_weight"],
        },
    ),
    ("sampling_strategy_item_trait", ty.Any, {"help_string": ""}),
    ("sampling_strategy_stage_trait", ty.Any, {"help_string": ""}),
    (
        "sampling_strategy",
        list,
        {
            "help_string": "the metric sampling strategy (strategies) for each stage",
            "requires": ["metric_weight"],
        },
    ),
    ("sampling_percentage_item_trait", ty.Any, {"help_string": ""}),
    ("sampling_percentage_stage_trait", ty.Any, {"help_string": ""}),
    (
        "sampling_percentage",
        list,
        {
            "help_string": "the metric sampling percentage(s) to use for each stage",
            "requires": ["sampling_strategy"],
        },
    ),
    ("use_estimate_learning_rate_once", list, {"help_string": ""}),
    (
        "use_histogram_matching",
        ty.Any,
        True,
        {"help_string": "Histogram match the images before registration."},
    ),
    (
        "interpolation",
        ty.Any,
        "Linear",
        {"help_string": "", "argstr": "{interpolation}"},
    ),
    ("interpolation_parameters", ty.Any, {"help_string": ""}),
    (
        "write_composite_transform",
        bool,
        False,
        {
            "help_string": "",
            "argstr": "--write-composite-transform {write_composite_transform}",
        },
    ),
    (
        "collapse_output_transforms",
        bool,
        True,
        {
            "help_string": "Collapse output transforms. Specifically, enabling this option combines all adjacent linear transforms and composes all adjacent displacement field transforms before writing the results to disk.",
            "argstr": "--collapse-output-transforms {collapse_output_transforms}",
        },
    ),
    (
        "initialize_transforms_per_stage",
        bool,
        False,
        {
            "help_string": "Initialize linear transforms from the previous stage. By enabling this option, the current linear stage transform is directly initialized from the previous stages linear transform; this allows multiple linear stages to be run where each stage directly updates the estimated linear transform from the previous stage. (e.g. Translation -> Rigid -> Affine). ",
            "argstr": "--initialize-transforms-per-stage {initialize_transforms_per_stage}",
        },
    ),
    (
        "float",
        bool,
        {
            "help_string": "Use float instead of double for computations.",
            "argstr": "--float {float}",
        },
    ),
    (
        "transforms",
        list,
        {"help_string": "", "argstr": "{transforms}", "mandatory": True},
    ),
    ("transform_parameters", list, {"help_string": ""}),
    (
        "restrict_deformation",
        list,
        {
            "help_string": "This option allows the user to restrict the optimization of the displacement field, translation, rigid or affine transform on a per-component basis. For example, if one wants to limit the deformation or rotation of 3-D volume to the  first two dimensions, this is possible by specifying a weight vector of '1x1x0' for a deformation field or '1x1x0x1x1x0' for a rigid transformation.  Low-dimensional restriction only works if there are no preceding transformations."
        },
    ),
    ("number_of_iterations", list, {"help_string": ""}),
    ("smoothing_sigmas", list, {"help_string": "", "mandatory": True}),
    (
        "sigma_units",
        list,
        {"help_string": "units for smoothing sigmas", "requires": ["smoothing_sigmas"]},
    ),
    ("shrink_factors", list, {"help_string": "", "mandatory": True}),
    (
        "convergence_threshold",
        list,
        [1e-06],
        {"help_string": "", "requires": ["number_of_iterations"]},
    ),
    (
        "convergence_window_size",
        list,
        [10],
        {"help_string": "", "requires": ["convergence_threshold"]},
    ),
    (
        "output_transform_prefix",
        str,
        "transform",
        {"help_string": "", "argstr": "{output_transform_prefix}"},
    ),
    ("output_warped_image", ty.Any, {"help_string": ""}),
    (
        "output_inverse_warped_image",
        ty.Any,
        {"help_string": "", "requires": ["output_warped_image"]},
    ),
    (
        "winsorize_upper_quantile",
        ty.Any,
        1.0,
        {
            "help_string": "The Upper quantile to clip image ranges",
            "argstr": "{winsorize_upper_quantile}",
        },
    ),
    (
        "winsorize_lower_quantile",
        ty.Any,
        0.0,
        {
            "help_string": "The Lower quantile to clip image ranges",
            "argstr": "{winsorize_lower_quantile}",
        },
    ),
    (
        "random_seed",
        int,
        {
            "help_string": "Fixed seed for random number generation",
            "argstr": "--random-seed {random_seed}",
        },
    ),
    ("verbose", bool, False, {"help_string": "", "argstr": "-v"}),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
Registration_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "forward_transforms",
        ty.List[File],
        {"help_string": "List of output transforms for forward registration"},
    ),
    (
        "reverse_forward_transforms",
        ty.List[File],
        {
            "help_string": "List of output transforms for forward registration reversed for antsApplyTransform"
        },
    ),
    (
        "reverse_transforms",
        ty.List[File],
        {"help_string": "List of output transforms for reverse registration"},
    ),
    (
        "forward_invert_flags",
        list,
        {"help_string": "List of flags corresponding to the forward transforms"},
    ),
    (
        "reverse_forward_invert_flags",
        list,
        {
            "help_string": "List of flags corresponding to the forward transforms reversed for antsApplyTransform"
        },
    ),
    (
        "reverse_invert_flags",
        list,
        {"help_string": "List of flags corresponding to the reverse transforms"},
    ),
    ("composite_transform", File, {"help_string": "Composite transform file"}),
    (
        "inverse_composite_transform",
        File,
        {"help_string": "Inverse composite transform file"},
    ),
    (
        "warped_image",
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
        {"help_string": "Outputs warped image"},
    ),
    (
        "inverse_warped_image",
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
        {"help_string": "Outputs the inverse of the warped image"},
    ),
    (
        "save_state",
        TextMatrix,
        {"help_string": "The saved registration state to be restored"},
    ),
    (
        "metric_value",
        float,
        {
            "help_string": "the final value of metric",
            "callable": "metric_value_callable",
        },
    ),
    (
        "elapsed_time",
        float,
        {
            "help_string": "the total elapsed time as reported by ANTs",
            "callable": "elapsed_time_callable",
        },
    ),
]
Registration_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Registration(ShellCommandTask):
    """
    Examples
    -------

    >>> import copy
    >>> from fileformats.application import Dicom
    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> import pprint
    >>> from pydra.engine.specs import MultiInputObj
    >>> from pydra.tasks.ants.auto.registration.registration import Registration

    >>> task = Registration()
    >>> task.inputs.dimension = 3
    >>> task.inputs.fixed_image = "fixed1.nii"
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image = "moving1.nii"
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.initial_moving_transform = [TextMatrix.mock("t"), TextMatrix.mock("r"), TextMatrix.mock("a"), TextMatrix.mock("n"), TextMatrix.mock("s"), TextMatrix.mock("."), TextMatrix.mock("m"), TextMatrix.mock("a"), TextMatrix.mock("t")]
    >>> task.inputs.metric = ["Mattes"]*2
    >>> task.inputs.metric_weight = [1]*2 # Default (value ignored currently by ANTs)
    >>> task.inputs.radius_or_number_of_bins = [32]*2
    >>> task.inputs.sampling_strategy = ["Random", None]
    >>> task.inputs.sampling_percentage = [0.05, None]
    >>> task.inputs.use_estimate_learning_rate_once = [True, True]
    >>> task.inputs.use_histogram_matching = [True, True] # This is the default
    >>> task.inputs.write_composite_transform = True
    >>> task.inputs.collapse_output_transforms = False
    >>> task.inputs.initialize_transforms_per_stage = False
    >>> task.inputs.transforms = ["Affine", "SyN"]
    >>> task.inputs.transform_parameters = [(2.0,), (0.25, 3.0, 0.0)]
    >>> task.inputs.number_of_iterations = [[1500, 200], [100, 50, 30]]
    >>> task.inputs.smoothing_sigmas = [[1,0], [2,1,0]]
    >>> task.inputs.sigma_units = ["vox"] * 2
    >>> task.inputs.shrink_factors = [[2,1], [3,2,1]]
    >>> task.inputs.convergence_threshold = [1.e-8, 1.e-9]
    >>> task.inputs.convergence_window_size = [20]*2
    >>> task.inputs.output_transform_prefix = "output_"
    >>> task.inputs.output_warped_image = "output_warped_image.nii.gz"
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 0 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.invert_initial_moving_transform = True
    >>> task.inputs.winsorize_lower_quantile = 0.025
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.025, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.winsorize_upper_quantile = 0.975
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 0.975 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.winsorize_upper_quantile = 0.975
    >>> task.inputs.winsorize_lower_quantile = 0.025
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.025, 0.975 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.float = True
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --float 1 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.float = False
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --float 0 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.save_state = "trans.mat"
    >>> task.inputs.restore_state = TextMatrix.mock("trans.mat")
    >>> task.inputs.collapse_output_transforms = True
    >>> task.inputs.initialize_transforms_per_stage = True
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 1 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 1 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --restore-state trans.mat --save-state trans.mat --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.write_composite_transform = False
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 1 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 1 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --restore-state trans.mat --save-state trans.mat --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 0'


    >>> task = Registration()
    >>> task.inputs.fixed_image = "fixed1.nii"
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image = "moving1.nii"
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.metric = ["Mattes", ["Mattes", "CC"]]
    >>> task.inputs.metric_weight = [1, [.5,.5]]
    >>> task.inputs.radius_or_number_of_bins = [32, [32, 4] ]
    >>> task.inputs.sampling_strategy = ["Random", None] # use default strategy in second stage
    >>> task.inputs.sampling_percentage = [0.05, [0.05, 0.10]]
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 0.5, 32, None, 0.05 ] --metric CC[ fixed1.nii, moving1.nii, 0.5, 4, None, 0.1 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image = ["fixed1.nii", "fixed2.nii"]
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image = ["moving1.nii", "moving2.nii"]
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 0.5, 32, None, 0.05 ] --metric CC[ fixed2.nii, moving2.nii, 0.5, 4, None, 0.1 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.interpolation = "BSpline"
    >>> task.inputs.interpolation_parameters = (3,)
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation BSpline[ 3 ] --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.interpolation = "Gaussian"
    >>> task.inputs.interpolation_parameters = (1.0, 1.0)
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Gaussian[ 1.0, 1.0 ] --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.transforms = ["Affine", "BSplineSyN"]
    >>> task.inputs.transform_parameters = [(2.0,), (0.25, 26, 0, 3)]
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform BSplineSyN[ 0.25, 26, 0, 3 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.fixed_image_masks = ["NULL", "fixed1.nii"]
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --masks [ NULL, NULL ] --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --masks [ fixed1.nii, NULL ] --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    >>> task = Registration()
    >>> task.inputs.fixed_image_mask = File.mock()
    >>> task.inputs.moving_image_mask = File.mock()
    >>> task.inputs.restore_state = TextMatrix.mock()
    >>> task.inputs.initial_moving_transform = [TextMatrix.mock("func_to_struct.mat"), TextMatrix.mock("ants_Warp.nii.gz")]
    >>> task.inputs.invert_initial_moving_transform = [False, False]
    >>> task.cmdline
    'antsRegistration --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ func_to_struct.mat, 0 ] [ ants_Warp.nii.gz, 0 ] --initialize-transforms-per-stage 0 --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ] --write-composite-transform 1'


    """

    input_spec = Registration_input_spec
    output_spec = Registration_output_spec
    executable = "antsRegistration"
