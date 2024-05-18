from fileformats.medimage import NiftiGz
import logging
from pydra.engine import ShellCommandTask, specs


logger = logging.getLogger(__name__)


input_fields = [
    (
        "input_wm",
        NiftiGz,
        {
            "help_string": "white matter segmentation image",
            "argstr": "{input_wm}",
            "copyfile": True,
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "input_gm",
        NiftiGz,
        {
            "help_string": "gray matter segmentation image",
            "argstr": "{input_gm}",
            "copyfile": True,
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "output_image",
        str,
        {
            "help_string": "name of output file",
            "argstr": "{output_image}",
            "position": 3,
            "output_file_template": "{input_wm}_thickness",
        },
    ),
    (
        "smooth_param",
        float,
        {
            "help_string": "Sigma of the Laplacian Recursive Image Filter (defaults to 1)",
            "argstr": "{smooth_param}",
            "position": 4,
        },
    ),
    (
        "prior_thickness",
        float,
        {
            "help_string": "Prior thickness (defaults to 500)",
            "argstr": "{prior_thickness}",
            "position": 5,
            "requires": ["smooth_param"],
        },
    ),
    (
        "dT",
        float,
        {
            "help_string": "Time delta used during integration (defaults to 0.01)",
            "argstr": "{dT}",
            "position": 6,
            "requires": ["prior_thickness"],
        },
    ),
    (
        "sulcus_prior",
        float,
        {
            "help_string": "Positive floating point number for sulcus prior. Authors said that 0.15 might be a reasonable value",
            "argstr": "{sulcus_prior}",
            "position": 7,
            "requires": ["dT"],
        },
    ),
    (
        "tolerance",
        float,
        {
            "help_string": "Tolerance to reach during optimization (defaults to 0.001)",
            "argstr": "{tolerance}",
            "position": 8,
            "requires": ["sulcus_prior"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
LaplacianThickness_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
LaplacianThickness_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class LaplacianThickness(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.medimage import NiftiGz
    >>> from pydra.tasks.ants.auto.segmentation.laplacian_thickness import LaplacianThickness

    >>> task = LaplacianThickness()
    >>> task.inputs.input_wm = NiftiGz.mock("white_matter.nii.gz")
    >>> task.inputs.input_gm = NiftiGz.mock("gray_matter.nii.gz")
    >>> task.cmdline
    'LaplacianThickness white_matter.nii.gz gray_matter.nii.gz white_matter_thickness.nii.gz'


    >>> task = LaplacianThickness()
    >>> task.inputs.input_wm = NiftiGz.mock()
    >>> task.inputs.input_gm = NiftiGz.mock()
    >>> task.inputs.output_image = "output_thickness.nii.gz"
    >>> task.cmdline
    'LaplacianThickness white_matter.nii.gz gray_matter.nii.gz output_thickness.nii.gz'


    """

    input_spec = LaplacianThickness_input_spec
    output_spec = LaplacianThickness_output_spec
    executable = "LaplacianThickness"
