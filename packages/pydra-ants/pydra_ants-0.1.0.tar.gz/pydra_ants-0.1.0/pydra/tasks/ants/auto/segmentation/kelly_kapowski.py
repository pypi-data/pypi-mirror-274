from fileformats.application import Dicom
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "dimension",
        ty.Any,
        3,
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "--image-dimensionality {dimension}",
        },
    ),
    (
        "segmentation_image",
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
            "help_string": "A segmentation image must be supplied labeling the gray and white matters. Default values = 2 and 3, respectively.",
            "argstr": '--segmentation-image "{segmentation_image}"',
            "mandatory": True,
        },
    ),
    (
        "gray_matter_label",
        int,
        2,
        {
            "help_string": "The label value for the gray matter label in the segmentation_image."
        },
    ),
    (
        "white_matter_label",
        int,
        3,
        {
            "help_string": "The label value for the white matter label in the segmentation_image."
        },
    ),
    (
        "gray_matter_prob_image",
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
            "help_string": "In addition to the segmentation image, a gray matter probability image can be used. If no such image is supplied, one is created using the segmentation image and a variance of 1.0 mm.",
            "argstr": '--gray-matter-probability-image "{gray_matter_prob_image}"',
        },
    ),
    (
        "white_matter_prob_image",
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
            "help_string": "In addition to the segmentation image, a white matter probability image can be used. If no such image is supplied, one is created using the segmentation image and a variance of 1.0 mm.",
            "argstr": '--white-matter-probability-image "{white_matter_prob_image}"',
        },
    ),
    (
        "convergence",
        str,
        "[50,0.001,10]",
        {
            "help_string": "Convergence is determined by fitting a line to the normalized energy profile of the last N iterations (where N is specified by the window size) and determining the slope which is then compared with the convergence threshold.",
            "argstr": '--convergence "{convergence}"',
        },
    ),
    (
        "thickness_prior_estimate",
        float,
        10,
        {
            "help_string": "Provides a prior constraint on the final thickness measurement in mm.",
            "argstr": "--thickness-prior-estimate {thickness_prior_estimate}",
        },
    ),
    (
        "thickness_prior_image",
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
            "help_string": "An image containing spatially varying prior thickness values.",
            "argstr": '--thickness-prior-image "{thickness_prior_image}"',
        },
    ),
    (
        "gradient_step",
        float,
        0.025,
        {
            "help_string": "Gradient step size for the optimization.",
            "argstr": "--gradient-step {gradient_step}",
        },
    ),
    (
        "smoothing_variance",
        float,
        1.0,
        {
            "help_string": "Defines the Gaussian smoothing of the hit and total images.",
            "argstr": "--smoothing-variance {smoothing_variance}",
        },
    ),
    (
        "smoothing_velocity_field",
        float,
        1.5,
        {
            "help_string": "Defines the Gaussian smoothing of the velocity field (default = 1.5). If the b-spline smoothing option is chosen, then this defines the isotropic mesh spacing for the smoothing spline (default = 15).",
            "argstr": "--smoothing-velocity-field-parameter {smoothing_velocity_field}",
        },
    ),
    (
        "use_bspline_smoothing",
        bool,
        {
            "help_string": "Sets the option for B-spline smoothing of the velocity field.",
            "argstr": "--use-bspline-smoothing 1",
        },
    ),
    (
        "number_integration_points",
        int,
        10,
        {
            "help_string": "Number of compositions of the diffeomorphism per iteration.",
            "argstr": "--number-of-integration-points {number_integration_points}",
        },
    ),
    (
        "max_invert_displacement_field_iters",
        int,
        20,
        {
            "help_string": "Maximum number of iterations for estimating the invertdisplacement field.",
            "argstr": "--maximum-number-of-invert-displacement-field-iterations {max_invert_displacement_field_iters}",
        },
    ),
    (
        "cortical_thickness",
        Path,
        {
            "help_string": "Filename for the cortical thickness.",
            "argstr": '--output "{cortical_thickness}"',
            "output_file_template": "{segmentation_image}_cortical_thickness",
        },
    ),
    (
        "warped_white_matter",
        Path,
        {
            "help_string": "Filename for the warped white matter file.",
            "output_file_template": "{segmentation_image}_warped_white_matter",
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
KellyKapowski_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
KellyKapowski_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class KellyKapowski(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.kelly_kapowski import KellyKapowski

    >>> task = KellyKapowski()
    >>> task.inputs.dimension = 3
    >>> task.inputs.segmentation_image = "segmentation0.nii.gz"
    >>> task.inputs.convergence = "[45,0.0,10]"
    >>> task.inputs.thickness_prior_estimate = 10
    >>> task.cmdline
    'KellyKapowski --convergence "[45,0.0,10]" --output "[segmentation0_cortical_thickness.nii.gz,segmentation0_warped_white_matter.nii.gz]" --image-dimensionality 3 --gradient-step 0.025000 --maximum-number-of-invert-displacement-field-iterations 20 --number-of-integration-points 10 --segmentation-image "[segmentation0.nii.gz,2,3]" --smoothing-variance 1.000000 --smoothing-velocity-field-parameter 1.500000 --thickness-prior-estimate 10.000000'


    """

    input_spec = KellyKapowski_input_spec
    output_spec = KellyKapowski_output_spec
    executable = "KellyKapowski"
