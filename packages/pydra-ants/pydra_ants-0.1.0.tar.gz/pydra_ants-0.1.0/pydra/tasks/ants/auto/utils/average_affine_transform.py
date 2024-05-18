from fileformats.datascience import TextMatrix
from fileformats.generic import File
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
        "output_affine_transform",
        Path,
        {
            "help_string": "Outputfname.txt: the name of the resulting transform.",
            "argstr": "{output_affine_transform}",
            "mandatory": True,
            "position": 1,
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
AverageAffineTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("affine_transform", File, {"help_string": "average transform file"})]
AverageAffineTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class AverageAffineTransform(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from pydra.tasks.ants.auto.utils.average_affine_transform import AverageAffineTransform

    >>> task = AverageAffineTransform()
    >>> task.inputs.dimension = 3
    >>> task.inputs.output_affine_transform = "MYtemplatewarp.mat"
    >>> task.inputs.transforms = [TextMatrix.mock("trans.mat"), TextMatrix.mock("func_to_struct.mat")]
    >>> task.cmdline
    'AverageAffineTransform 3 MYtemplatewarp.mat trans.mat func_to_struct.mat'


    """

    input_spec = AverageAffineTransform_input_spec
    output_spec = AverageAffineTransform_output_spec
    executable = "AverageAffineTransform"
