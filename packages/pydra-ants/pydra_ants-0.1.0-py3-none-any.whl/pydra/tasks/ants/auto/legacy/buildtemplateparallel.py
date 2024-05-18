from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
    (
        "dimension",
        ty.Any,
        3,
        {
            "help_string": "image dimension (2, 3 or 4)",
            "argstr": "-d {dimension}",
            "position": 1,
        },
    ),
    (
        "out_prefix",
        str,
        "antsTMPL_",
        {
            "help_string": "Prefix that is prepended to all output files (default = antsTMPL_)",
            "argstr": "-o {out_prefix}",
        },
    ),
    (
        "in_files",
        ty.List[Nifti1],
        {
            "help_string": "list of images to generate template from",
            "argstr": "{in_files}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "parallelization",
        ty.Any,
        0,
        {
            "help_string": "control for parallel processing (0 = serial, 1 = use PBS, 2 = use PEXEC, 3 = use Apple XGrid",
            "argstr": "-c {parallelization}",
        },
    ),
    (
        "gradient_step_size",
        float,
        {
            "help_string": "smaller magnitude results in more cautious steps (default = .25)",
            "argstr": "-g {gradient_step_size}",
        },
    ),
    (
        "iteration_limit",
        int,
        4,
        {
            "help_string": "iterations of template construction",
            "argstr": "-i {iteration_limit}",
        },
    ),
    (
        "num_cores",
        int,
        {
            "help_string": "Requires parallelization = 2 (PEXEC). Sets number of cpu cores to use",
            "argstr": "-j {num_cores}",
            "requires": ["parallelization"],
        },
    ),
    (
        "max_iterations",
        list,
        {
            "help_string": "maximum number of iterations (must be list of integers in the form [J,K,L...]: J = coarsest resolution iterations, K = middle resolution iterations, L = fine resolution iterations",
            "argstr": "-m {max_iterations}",
            "sep": "x",
        },
    ),
    (
        "bias_field_correction",
        bool,
        {
            "help_string": "Applies bias field correction to moving image",
            "argstr": "-n 1",
        },
    ),
    (
        "rigid_body_registration",
        bool,
        {
            "help_string": "registers inputs before creating template (useful if no initial template available)",
            "argstr": "-r 1",
        },
    ),
    (
        "similarity_metric",
        ty.Any,
        {
            "help_string": "Type of similartiy metric used for registration (CC = cross correlation, MI = mutual information, PR = probability mapping, MSQ = mean square difference)",
            "argstr": "-s {similarity_metric}",
        },
    ),
    (
        "transformation_model",
        ty.Any,
        "GR",
        {
            "help_string": "Type of transofmration model used for registration (EL = elastic transformation model, SY = SyN with time, arbitrary number of time points, S2 =  SyN with time optimized for 2 time points, GR = greedy SyN, EX = exponential, DD = diffeomorphic demons style exponential mapping",
            "argstr": "-t {transformation_model}",
        },
    ),
    (
        "use_first_as_target",
        bool,
        {
            "help_string": "uses first volume as target of all inputs. When not used, an unbiased average image is used to start."
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
buildtemplateparallel_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("final_template_file", File, {"help_string": "final ANTS template"}),
    (
        "template_files",
        ty.List[File],
        {"help_string": "Templates from different stages of iteration"},
    ),
    (
        "subject_outfiles",
        ty.List[File],
        {
            "help_string": "Outputs for each input image. Includes warp field, inverse warp, Affine, original image (repaired) and warped image (deformed)"
        },
    ),
]
buildtemplateparallel_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class buildtemplateparallel(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.ants.auto.legacy.buildtemplateparallel import buildtemplateparallel

    >>> task = buildtemplateparallel()
    >>> task.inputs.in_files = [Nifti1.mock("T1.nii"), Nifti1.mock("structural.nii")]
    >>> task.inputs.max_iterations = [30, 90, 20]
    >>> task.cmdline
    'buildtemplateparallel.sh -d 3 -i 4 -m 30x90x20 -o antsTMPL_ -c 0 -t GR T1.nii structural.nii'


    """

    input_spec = buildtemplateparallel_input_spec
    output_spec = buildtemplateparallel_output_spec
    executable = "buildtemplateparallel.sh"
