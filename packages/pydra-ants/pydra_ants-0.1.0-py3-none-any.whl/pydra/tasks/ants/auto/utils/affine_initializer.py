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
        ty.Any,
        3,
        {"help_string": "dimension", "argstr": "{dimension}", "position": 0},
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
        {
            "help_string": "reference image",
            "argstr": "{fixed_image}",
            "mandatory": True,
            "position": 1,
        },
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
            "help_string": "moving image",
            "argstr": "{moving_image}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "out_file",
        Path,
        "transform.mat",
        {"help_string": "output transform file", "argstr": "{out_file}", "position": 3},
    ),
    (
        "search_factor",
        float,
        15.0,
        {
            "help_string": "increments (degrees) for affine search",
            "argstr": "{search_factor}",
            "position": 4,
        },
    ),
    (
        "radian_fraction",
        ty.Any,
        0.1,
        {
            "help_string": "search this arc +/- principal axes",
            "argstr": "{radian_fraction}",
            "position": 5,
        },
    ),
    (
        "principal_axes",
        bool,
        False,
        {
            "help_string": "whether the rotation is searched around an initial principal axis alignment.",
            "argstr": "{principal_axes}",
            "position": 6,
        },
    ),
    (
        "local_search",
        int,
        10,
        {
            "help_string": " determines if a local optimization is run at each search point for the set number of iterations",
            "argstr": "{local_search}",
            "position": 7,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
AffineInitializer_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("out_file", File, {"help_string": "output transform file"})]
AffineInitializer_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AffineInitializer(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.affine_initializer import AffineInitializer

    >>> task = AffineInitializer()
    >>> task.inputs.fixed_image = "fixed1.nii"
    >>> task.inputs.moving_image = "moving1.nii"
    >>> task.cmdline
    'antsAffineInitializer 3 fixed1.nii moving1.nii transform.mat 15.000000 0.100000 0 10'


    """

    input_spec = AffineInitializer_input_spec
    output_spec = AffineInitializer_output_spec
    executable = "antsAffineInitializer"
