from fileformats.application import Dicom
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
            "mandatory": True,
            "position": 0,
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
            "help_string": "Main input is a 3-D grayscale image.",
            "argstr": "{input_image}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "output_image",
        str,
        "rgb.nii.gz",
        {"help_string": "rgb output image", "argstr": "{output_image}", "position": 2},
    ),
    (
        "mask_image",
        ty.Any,
        "none",
        {"help_string": "mask image", "argstr": "{mask_image}", "position": 3},
    ),
    (
        "colormap",
        ty.Any,
        {
            "help_string": "Select a colormap",
            "argstr": "{colormap}",
            "mandatory": True,
            "position": 4,
        },
    ),
    (
        "custom_color_map_file",
        str,
        "none",
        {
            "help_string": "custom color map file",
            "argstr": "{custom_color_map_file}",
            "position": 5,
        },
    ),
    (
        "minimum_input",
        int,
        {
            "help_string": "minimum input",
            "argstr": "{minimum_input}",
            "mandatory": True,
            "position": 6,
        },
    ),
    (
        "maximum_input",
        int,
        {
            "help_string": "maximum input",
            "argstr": "{maximum_input}",
            "mandatory": True,
            "position": 7,
        },
    ),
    (
        "minimum_RGB_output",
        int,
        0,
        {"help_string": "", "argstr": "{minimum_RGB_output}", "position": 8},
    ),
    (
        "maximum_RGB_output",
        int,
        255,
        {"help_string": "", "argstr": "{maximum_RGB_output}", "position": 9},
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ConvertScalarImageToRGB_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "output_image",
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
        {"help_string": "converted RGB image"},
    )
]
ConvertScalarImageToRGB_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ConvertScalarImageToRGB(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.visualization.convert_scalar_image_to_rgb import ConvertScalarImageToRGB

    >>> task = ConvertScalarImageToRGB()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "T1.nii.gz"
    >>> task.inputs.colormap = "jet"
    >>> task.inputs.minimum_input = 0
    >>> task.inputs.maximum_input = 6
    >>> task.cmdline
    'ConvertScalarImageToRGB 3 T1.nii.gz rgb.nii.gz none jet none 0 6 0 255'


    """

    input_spec = ConvertScalarImageToRGB_input_spec
    output_spec = ConvertScalarImageToRGB_output_spec
    executable = "ConvertScalarImageToRGB"
