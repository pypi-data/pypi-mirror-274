from fileformats.datascience import Hdf5, TextMatrix
from fileformats.generic import File
import logging
from pathlib import Path
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "process",
        ty.Any,
        "assemble",
        {
            "help_string": "What to do with the transform inputs (assemble or disassemble)",
            "argstr": "--{process}",
            "position": 1,
        },
    ),
    (
        "out_file",
        Path,
        {
            "help_string": "Output file path (only used for disassembly).",
            "argstr": "{out_file}",
            "position": 2,
        },
    ),
    (
        "in_file",
        ty.List[ty.Union[TextMatrix, Hdf5]],
        {
            "help_string": "Input transform file(s)",
            "argstr": "{in_file}...",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "output_prefix",
        str,
        "transform",
        {
            "help_string": "A prefix that is prepended to all output files (only used for assembly).",
            "argstr": "{output_prefix}",
            "position": 4,
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
CompositeTransformUtil_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("affine_transform", File, {"help_string": "Affine transform component"}),
    ("displacement_field", File, {"help_string": "Displacement field component"}),
    ("out_file", Hdf5, {"help_string": "Compound transformation file"}),
]
CompositeTransformUtil_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CompositeTransformUtil(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import Hdf5, TextMatrix
    >>> from fileformats.generic import File
    >>> from pydra.tasks.ants.auto.registration.composite_transform_util import CompositeTransformUtil

    >>> task = CompositeTransformUtil()
    >>> task.inputs.process = "disassemble"
    >>> task.inputs.in_file = "output_Composite.h5"
    >>> task.cmdline
    'CompositeTransformUtil --disassemble output_Composite.h5 transform'


    >>> task = CompositeTransformUtil()
    >>> task.inputs.process = "assemble"
    >>> task.inputs.out_file = "my.h5"
    >>> task.inputs.in_file = ["AffineTransform.mat", "DisplacementFieldTransform.nii.gz"]
    >>> task.cmdline
    'CompositeTransformUtil --assemble my.h5 AffineTransform.mat DisplacementFieldTransform.nii.gz '


    """

    input_spec = CompositeTransformUtil_input_spec
    output_spec = CompositeTransformUtil_output_spec
    executable = "CompositeTransformUtil"
