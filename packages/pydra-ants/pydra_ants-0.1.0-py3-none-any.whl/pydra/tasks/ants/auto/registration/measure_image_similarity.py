from fileformats.application import Dicom
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


def similarity_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["similarity"]


input_fields = [
    (
        "dimension",
        ty.Any,
        {
            "help_string": "Dimensionality of the fixed/moving image pair",
            "argstr": "--dimensionality {dimension}",
            "position": 1,
        },
    ),
    (
        "fixed_image",
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
        {"help_string": "Image to which the moving image is warped", "mandatory": True},
    ),
    (
        "moving_image",
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
            "help_string": "Image to apply transformation to (generally a coregistered functional)",
            "mandatory": True,
        },
    ),
    ("metric", ty.Any, {"help_string": "", "argstr": "{metric}", "mandatory": True}),
    (
        "metric_weight",
        float,
        1.0,
        {
            "help_string": 'The "metricWeight" variable is not used.',
            "requires": ["metric"],
        },
    ),
    (
        "radius_or_number_of_bins",
        int,
        {
            "help_string": "The number of bins in each stage for the MI and Mattes metric, or the radius for other metrics",
            "mandatory": True,
            "requires": ["metric"],
        },
    ),
    (
        "sampling_strategy",
        ty.Any,
        "None",
        {
            "help_string": 'Manner of choosing point set over which to optimize the metric. Defaults to "None" (i.e. a dense sampling of one sample per voxel).',
            "requires": ["metric"],
        },
    ),
    (
        "sampling_percentage",
        ty.Any,
        {
            "help_string": "Percentage of points accessible to the sampling strategy over which to optimize the metric.",
            "mandatory": True,
            "requires": ["metric"],
        },
    ),
    (
        "fixed_image_mask",
        Nifti1,
        {
            "help_string": "mask used to limit metric sampling region of the fixed image",
            "argstr": "{fixed_image_mask}",
        },
    ),
    (
        "moving_image_mask",
        NiftiGz,
        {
            "help_string": "mask used to limit metric sampling region of the moving image",
            "requires": ["fixed_image_mask"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
MeasureImageSimilarity_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("similarity", float, {"callable": "similarity_callable"})]
MeasureImageSimilarity_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MeasureImageSimilarity(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.registration.measure_image_similarity import MeasureImageSimilarity

    >>> task = MeasureImageSimilarity()
    >>> task.inputs.dimension = 3
    >>> task.inputs.fixed_image = "T1.nii"
    >>> task.inputs.moving_image = "resting.nii"
    >>> task.inputs.metric = "MI"
    >>> task.inputs.metric_weight = 1.0
    >>> task.inputs.radius_or_number_of_bins = 5
    >>> task.inputs.sampling_strategy = "Regular"
    >>> task.inputs.sampling_percentage = 1.0
    >>> task.inputs.fixed_image_mask = Nifti1.mock("mask.nii")
    >>> task.inputs.moving_image_mask = NiftiGz.mock("mask.nii.gz")
    >>> task.cmdline
    'MeasureImageSimilarity --dimensionality 3 --masks ["mask.nii","mask.nii.gz"] --metric MI["T1.nii","resting.nii",1.0,5,Regular,1.0]'


    """

    input_spec = MeasureImageSimilarity_input_spec
    output_spec = MeasureImageSimilarity_output_spec
    executable = "MeasureImageSimilarity"
