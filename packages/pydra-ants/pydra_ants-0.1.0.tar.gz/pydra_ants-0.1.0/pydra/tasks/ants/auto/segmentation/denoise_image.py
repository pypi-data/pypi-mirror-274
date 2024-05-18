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
            "help_string": "This option forces the image to be treated as a specified-dimensional image. If not specified, the program tries to infer the dimensionality from the input image.",
            "argstr": "-d {dimension}",
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
            "help_string": "A scalar image is expected as input for noise correction.",
            "argstr": "-i {input_image}",
            "mandatory": True,
        },
    ),
    (
        "noise_model",
        ty.Any,
        "Gaussian",
        {
            "help_string": "Employ a Rician or Gaussian noise model.",
            "argstr": "-n {noise_model}",
        },
    ),
    (
        "shrink_factor",
        int,
        1,
        {
            "help_string": "Running noise correction on large images can be time consuming. To lessen computation time, the input image can be resampled. The shrink factor, specified as a single integer, describes this resampling. Shrink factor = 1 is the default.",
            "argstr": "-s {shrink_factor}",
        },
    ),
    (
        "output_image",
        Path,
        {
            "help_string": "The output consists of the noise corrected version of the input image.",
            "argstr": "-o {output_image}",
            "output_file_template": "{input_image}_noise_corrected",
        },
    ),
    (
        "save_noise",
        bool,
        {
            "help_string": "True if the estimated noise should be saved to file.",
            "mandatory": True,
            "xor": ["noise_image"],
        },
    ),
    (
        "noise_image",
        Path,
        {
            "help_string": "Filename for the estimated noise.",
            "output_file_template": "{input_image}_noise",
        },
    ),
    ("verbose", bool, {"help_string": "Verbose output.", "argstr": "-v"}),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
DenoiseImage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
DenoiseImage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DenoiseImage(ShellCommandTask):
    """
    Examples
    -------

    >>> import copy
    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.denoise_image import DenoiseImage

    >>> task = DenoiseImage()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "im1.nii"
    >>> task.cmdline
    'DenoiseImage -d 3 -i im1.nii -n Gaussian -o im1_noise_corrected.nii -s 1'


    >>> task = DenoiseImage()
    >>> task.inputs.noise_model = "Rician"
    >>> task.inputs.shrink_factor = 2
    >>> task.inputs.output_image = "output_corrected_image.nii.gz"
    >>> task.cmdline
    'DenoiseImage -d 3 -i im1.nii -n Rician -o output_corrected_image.nii.gz -s 2'


    >>> task = DenoiseImage()
    >>> task.inputs.input_image = "im1.nii"
    >>> task.inputs.save_noise = True
    >>> task.cmdline
    'DenoiseImage -i im1.nii -n Gaussian -o [ im1_noise_corrected.nii, im1_noise.nii ] -s 1'


    """

    input_spec = DenoiseImage_input_spec
    output_spec = DenoiseImage_output_spec
    executable = "DenoiseImage"
