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
        "first_input",
        Nifti1,
        {
            "help_string": "image 1",
            "argstr": "{first_input}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "second_input",
        ty.Any,
        {
            "help_string": "image 2 or multiplication weight",
            "argstr": "{second_input}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "output_product_image",
        Path,
        {
            "help_string": "Outputfname.nii.gz: the name of the resulting image.",
            "argstr": "{output_product_image}",
            "mandatory": True,
            "position": 3,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
MultiplyImages_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "output_product_image",
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
MultiplyImages_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MultiplyImages(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.multiply_images import MultiplyImages

    >>> task = MultiplyImages()
    >>> task.inputs.dimension = 3
    >>> task.inputs.first_input = Nifti1.mock("moving2.nii")
    >>> task.inputs.second_input = 0.25
    >>> task.inputs.output_product_image = "out.nii"
    >>> task.cmdline
    'MultiplyImages 3 moving2.nii 0.25 out.nii'


    """

    input_spec = MultiplyImages_input_spec
    output_spec = MultiplyImages_output_spec
    executable = "MultiplyImages"
