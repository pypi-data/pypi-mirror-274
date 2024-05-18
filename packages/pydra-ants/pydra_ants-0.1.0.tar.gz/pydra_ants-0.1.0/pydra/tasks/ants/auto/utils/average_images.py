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
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "{dimension}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "output_average_image",
        Path,
        "average.nii",
        {
            "help_string": "the name of the resulting image.",
            "argstr": "{output_average_image}",
            "position": 1,
        },
    ),
    (
        "normalize",
        bool,
        {
            "help_string": "Normalize: if true, the 2nd image is divided by its mean. This will select the largest image to average into.",
            "argstr": "{normalize}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "images",
        ty.List[Nifti1],
        {
            "help_string": "image to apply transformation to (generally a coregistered functional)",
            "argstr": "{images}",
            "mandatory": True,
            "position": 3,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
AverageImages_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "output_average_image",
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
        {"help_string": "average image file"},
    )
]
AverageImages_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AverageImages(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.average_images import AverageImages

    >>> task = AverageImages()
    >>> task.inputs.dimension = 3
    >>> task.inputs.output_average_image = "average.nii.gz"
    >>> task.inputs.normalize = True
    >>> task.inputs.images = [Nifti1.mock("rc1s1.nii"), Nifti1.mock("rc1s1.nii")]
    >>> task.cmdline
    'AverageImages 3 average.nii.gz 1 rc1s1.nii rc1s1.nii'


    """

    input_spec = AverageImages_input_spec
    output_spec = AverageImages_output_spec
    executable = "AverageImages"
