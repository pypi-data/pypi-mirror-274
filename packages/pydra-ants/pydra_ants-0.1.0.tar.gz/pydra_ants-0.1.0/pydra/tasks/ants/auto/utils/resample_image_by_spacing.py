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
        "out_spacing",
        ty.Any,
        {
            "help_string": "output spacing",
            "argstr": "{out_spacing}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "apply_smoothing",
        bool,
        {
            "help_string": "smooth before resampling",
            "argstr": "{apply_smoothing}",
            "position": 5,
        },
    ),
    (
        "addvox",
        int,
        {
            "help_string": "addvox pads each dimension by addvox",
            "argstr": "{addvox}",
            "position": 6,
            "requires": ["apply_smoothing"],
        },
    ),
    (
        "nn_interp",
        bool,
        {
            "help_string": "nn interpolation",
            "argstr": "{nn_interp}",
            "position": -1,
            "requires": ["addvox"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ResampleImageBySpacing_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ResampleImageBySpacing_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ResampleImageBySpacing(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.resample_image_by_spacing import ResampleImageBySpacing

    >>> task = ResampleImageBySpacing()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.output_image = "output.nii.gz"
    >>> task.inputs.out_spacing = (4, 4, 4)
    >>> task.cmdline
    'None'


    >>> task = ResampleImageBySpacing()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.output_image = "output.nii.gz"
    >>> task.inputs.out_spacing = (4, 4, 4)
    >>> task.inputs.apply_smoothing = True
    >>> task.cmdline
    'None'


    >>> task = ResampleImageBySpacing()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.output_image = "output.nii.gz"
    >>> task.inputs.out_spacing = (0.4, 0.4, 0.4)
    >>> task.inputs.apply_smoothing = True
    >>> task.inputs.addvox = 2
    >>> task.inputs.nn_interp = False
    >>> task.cmdline
    'None'


    """

    input_spec = ResampleImageBySpacing_input_spec
    output_spec = ResampleImageBySpacing_output_spec
    executable = "ResampleImageBySpacing"
