from fileformats.medimage import Nifti1
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
        "output_image",
        Path,
        {
            "help_string": "output image file",
            "argstr": "{output_image}",
            "position": 2,
            "output_file_template": "{op1}_maths",
        },
    ),
    (
        "operation",
        ty.Any,
        {
            "help_string": "mathematical operations",
            "argstr": "{operation}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "op1",
        Nifti1,
        {
            "help_string": "first operator",
            "argstr": "{op1}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "op2",
        ty.Any,
        {"help_string": "second operator", "argstr": "{op2}", "position": -2},
    ),
    (
        "copy_header",
        bool,
        True,
        {
            "help_string": "copy headers of the original image into the output (corrected) file"
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ImageMath_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ImageMath_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ImageMath(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.ants.auto.utils.image_math import ImageMath

    >>> task = ImageMath()
    >>> task.inputs.operation = "+"
    >>> task.inputs.op1 = Nifti1.mock("structural.nii")
    >>> task.inputs.op2 = "2"
    >>> task.cmdline
    'ImageMath 3 structural_maths.nii + structural.nii 2'


    >>> task = ImageMath()
    >>> task.inputs.operation = "Project"
    >>> task.inputs.op1 = Nifti1.mock("structural.nii")
    >>> task.inputs.op2 = "1 2"
    >>> task.cmdline
    'ImageMath 3 structural_maths.nii Project structural.nii 1 2'


    >>> task = ImageMath()
    >>> task.inputs.operation = "G"
    >>> task.inputs.op1 = Nifti1.mock("structural.nii")
    >>> task.inputs.op2 = "4"
    >>> task.cmdline
    'ImageMath 3 structural_maths.nii G structural.nii 4'


    >>> task = ImageMath()
    >>> task.inputs.operation = "TruncateImageIntensity"
    >>> task.inputs.op1 = Nifti1.mock("structural.nii")
    >>> task.inputs.op2 = "0.005 0.999 256"
    >>> task.cmdline
    'ImageMath 3 structural_maths.nii TruncateImageIntensity structural.nii 0.005 0.999 256'


    """

    input_spec = ImageMath_input_spec
    output_spec = ImageMath_output_spec
    executable = "ImageMath"
