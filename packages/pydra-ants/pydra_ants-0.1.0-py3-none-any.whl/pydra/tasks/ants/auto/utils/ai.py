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
        {"help_string": "dimension of output image", "argstr": "-d {dimension}"},
    ),
    (
        "verbose",
        bool,
        False,
        {"help_string": "enable verbosity", "argstr": "-v {verbose}"},
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
            "help_string": "Image to which the moving_image should be transformed",
            "mandatory": True,
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
            "help_string": "Image that will be transformed to fixed_image",
            "mandatory": True,
        },
    ),
    (
        "fixed_image_mask",
        File,
        {"help_string": "fixed mage mask", "argstr": "-x {fixed_image_mask}"},
    ),
    (
        "moving_image_mask",
        File,
        {"help_string": "moving mage mask", "requires": ["fixed_image_mask"]},
    ),
    (
        "metric",
        ty.Any,
        {
            "help_string": "the metric(s) to use.",
            "argstr": "-m {metric}",
            "mandatory": True,
        },
    ),
    (
        "transform",
        ty.Any,
        ("Affine", 0.1),
        {
            "help_string": "Several transform options are available",
            "argstr": "-t {transform[0]}[{transform[1]}]",
        },
    ),
    (
        "principal_axes",
        bool,
        False,
        {
            "help_string": "align using principal axes",
            "argstr": "-p {principal_axes}",
            "xor": ["blobs"],
        },
    ),
    (
        "search_factor",
        ty.Any,
        (20, 0.12),
        {
            "help_string": "search factor",
            "argstr": "-s [{search_factor[0]},{search_factor[1]}]",
        },
    ),
    (
        "search_grid",
        ty.Any,
        {"help_string": "Translation search grid in mm", "argstr": "-g {search_grid}"},
    ),
    (
        "convergence",
        ty.Any,
        (10, 1e-06, 10),
        {
            "help_string": "convergence",
            "argstr": "-c [{convergence[0]},{convergence[1]},{convergence[2]}]",
        },
    ),
    (
        "output_transform",
        Path,
        "initialization.mat",
        {"help_string": "output file name", "argstr": "-o {output_transform}"},
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
AI_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("output_transform", File, {"help_string": "output file name"})]
AI_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AI(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.ai import AI

    """

    input_spec = AI_input_spec
    output_spec = AI_output_spec
    executable = "antsAI"
