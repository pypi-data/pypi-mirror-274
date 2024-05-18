from fileformats.application import Dicom
from fileformats.datascience import TextMatrix
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
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "{dimension}",
            "position": 0,
        },
    ),
    (
        "output_transform",
        Path,
        {
            "help_string": "the name of the resulting transform.",
            "argstr": "{output_transform}",
            "position": 1,
            "output_file_template": "{transforms}_composed",
        },
    ),
    (
        "reference_image",
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
            "help_string": "Reference image (only necessary when output is warpfield)",
            "argstr": "{reference_image}",
            "position": 2,
        },
    ),
    (
        "transforms",
        ty.List[TextMatrix],
        {
            "help_string": "transforms to average",
            "argstr": "{transforms}",
            "mandatory": True,
            "position": 3,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ComposeMultiTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ComposeMultiTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ComposeMultiTransform(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.compose_multi_transform import ComposeMultiTransform

    >>> task = ComposeMultiTransform()
    >>> task.inputs.dimension = 3
    >>> task.inputs.transforms = [TextMatrix.mock("struct_to_template.mat"), TextMatrix.mock("func_to_struct.mat")]
    >>> task.cmdline
    'ComposeMultiTransform 3 struct_to_template_composed.mat struct_to_template.mat func_to_struct.mat'


    """

    input_spec = ComposeMultiTransform_input_spec
    output_spec = ComposeMultiTransform_output_spec
    executable = "ComposeMultiTransform"
