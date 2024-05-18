from fileformats.application import Dicom
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "imageDimension",
        ty.Any,
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "{imageDimension}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "deformationField",
        NiftiGz,
        {
            "help_string": "deformation transformation file",
            "argstr": "{deformationField}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "outputImage",
        NiftiGz,
        {
            "help_string": "output filename",
            "argstr": "{outputImage}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "doLogJacobian",
        ty.Any,
        {
            "help_string": "return the log jacobian",
            "argstr": "{doLogJacobian}",
            "position": 3,
        },
    ),
    (
        "useGeometric",
        ty.Any,
        {
            "help_string": "return the geometric jacobian",
            "argstr": "{useGeometric}",
            "position": 4,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
CreateJacobianDeterminantImage_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "jacobian_image",
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
        {"help_string": "jacobian image"},
    )
]
CreateJacobianDeterminantImage_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CreateJacobianDeterminantImage(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.create_jacobian_determinant_image import CreateJacobianDeterminantImage

    >>> task = CreateJacobianDeterminantImage()
    >>> task.inputs.imageDimension = 3
    >>> task.inputs.deformationField = NiftiGz.mock("ants_Warp.nii.gz")
    >>> task.inputs.outputImage = NiftiGz.mock("out_name.nii.gz")
    >>> task.cmdline
    'CreateJacobianDeterminantImage 3 ants_Warp.nii.gz out_name.nii.gz'


    """

    input_spec = CreateJacobianDeterminantImage_input_spec
    output_spec = CreateJacobianDeterminantImage_output_spec
    executable = "CreateJacobianDeterminantImage"
