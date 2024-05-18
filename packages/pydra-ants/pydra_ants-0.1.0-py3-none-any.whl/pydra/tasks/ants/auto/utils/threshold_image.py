from fileformats.application import Dicom
from fileformats.generic import File
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
        int,
        3,
        {
            "help_string": "dimension of output image",
            "argstr": "{dimension}",
            "position": 1,
        },
    ),
    (
        "input_image",
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
            "help_string": "input image file",
            "argstr": "{input_image}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "output_image",
        Path,
        {
            "help_string": "output image file",
            "argstr": "{output_image}",
            "position": 3,
            "output_file_template": "{input_image}_resampled",
        },
    ),
    (
        "mode",
        ty.Any,
        {
            "help_string": "whether to run Otsu / Kmeans thresholding",
            "argstr": "{mode}",
            "position": 4,
            "requires": ["num_thresholds"],
            "xor": ["th_low", "th_high"],
        },
    ),
    (
        "num_thresholds",
        int,
        {
            "help_string": "number of thresholds",
            "argstr": "{num_thresholds}",
            "position": 5,
        },
    ),
    (
        "input_mask",
        File,
        {
            "help_string": "input mask for Otsu, Kmeans",
            "argstr": "{input_mask}",
            "requires": ["num_thresholds"],
        },
    ),
    (
        "th_low",
        float,
        {
            "help_string": "lower threshold",
            "argstr": "{th_low}",
            "position": 4,
            "xor": ["mode"],
        },
    ),
    (
        "th_high",
        float,
        {
            "help_string": "upper threshold",
            "argstr": "{th_high}",
            "position": 5,
            "xor": ["mode"],
        },
    ),
    (
        "inside_value",
        float,
        {
            "help_string": "inside value",
            "argstr": "{inside_value}",
            "position": 6,
            "requires": ["th_low"],
        },
    ),
    (
        "outside_value",
        float,
        {
            "help_string": "outside value",
            "argstr": "{outside_value}",
            "position": 7,
            "requires": ["th_low"],
        },
    ),
    (
        "copy_header",
        bool,
        {
            "help_string": "copy headers of the original image into the output (corrected) file",
            "mandatory": True,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ThresholdImage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ThresholdImage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ThresholdImage(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.threshold_image import ThresholdImage

    >>> task = ThresholdImage()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.output_image = "output.nii.gz"
    >>> task.inputs.input_mask = File.mock()
    >>> task.inputs.th_low = 0.5
    >>> task.inputs.th_high = 1.0
    >>> task.inputs.inside_value = 1.0
    >>> task.inputs.outside_value = 0.0
    >>> task.cmdline
    'None'


    >>> task = ThresholdImage()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.output_image = "output.nii.gz"
    >>> task.inputs.mode = "Kmeans"
    >>> task.inputs.num_thresholds = 4
    >>> task.inputs.input_mask = File.mock()
    >>> task.cmdline
    'None'


    """

    input_spec = ThresholdImage_input_spec
    output_spec = ThresholdImage_output_spec
    executable = "ThresholdImage"
