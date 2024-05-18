from fileformats.datascience import TextMatrix
from fileformats.text import Csv
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "dimension",
        ty.Any,
        {
            "help_string": "This option forces the image to be treated as a specified-dimensional image. If not specified, antsWarp tries to infer the dimensionality from the input image.",
            "argstr": "--dimensionality {dimension}",
        },
    ),
    (
        "input_file",
        Csv,
        {
            "help_string": "Currently, the only input supported is a csv file with columns including x,y (2D), x,y,z (3D) or x,y,z,t,label (4D) column headers. The points should be defined in physical space. If in doubt how to convert coordinates from your files to the space required by antsApplyTransformsToPoints try creating/drawing a simple label volume with only one voxel set to 1 and all others set to 0. Write down the voxel coordinates. Then use ImageMaths LabelStats to find out what coordinates for this voxel antsApplyTransformsToPoints is expecting.",
            "argstr": "--input {input_file}",
            "mandatory": True,
        },
    ),
    (
        "output_file",
        str,
        {
            "help_string": "Name of the output CSV file",
            "argstr": "--output {output_file}",
            "output_file_template": "{input_file}_transformed.csv",
        },
    ),
    (
        "transforms",
        ty.List[TextMatrix],
        {
            "help_string": "transforms that will be applied to the points",
            "argstr": "{transforms}",
            "mandatory": True,
        },
    ),
    (
        "invert_transform_flags",
        list,
        {"help_string": "list indicating if a transform should be reversed"},
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
ApplyTransformsToPoints_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyTransformsToPoints_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyTransformsToPoints(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.text import Csv
    >>> from pydra.tasks.ants.auto.resampling.apply_transforms_to_points import ApplyTransformsToPoints

    >>> task = ApplyTransformsToPoints()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_file = Csv.mock("moving.csv")
    >>> task.inputs.transforms = [TextMatrix.mock("trans.mat"), TextMatrix.mock("ants_Warp.nii.gz")]
    >>> task.inputs.invert_transform_flags = [False, False]
    >>> task.cmdline
    'antsApplyTransformsToPoints --dimensionality 3 --input moving.csv --output moving_transformed.csv --transform [ trans.mat, 0 ] --transform [ ants_Warp.nii.gz, 0 ]'


    """

    input_spec = ApplyTransformsToPoints_input_spec
    output_spec = ApplyTransformsToPoints_output_spec
    executable = "antsApplyTransformsToPoints"
