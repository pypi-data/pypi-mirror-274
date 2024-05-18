from fileformats.application import Dicom
from fileformats.generic import File
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
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
            "help_string": "image dimension (2 or 3)",
            "argstr": "-d {dimension}",
            "position": 1,
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
            "help_string": "template file to warp to",
            "argstr": "-r {reference_image}",
            "copyfile": True,
            "mandatory": True,
        },
    ),
    (
        "input_image",
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
            "help_string": "input image to warp to template",
            "argstr": "-i {input_image}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "force_proceed",
        bool,
        {
            "help_string": "force script to proceed even if headers may be incompatible",
            "argstr": "-f 1",
        },
    ),
    (
        "inverse_warp_template_labels",
        bool,
        {
            "help_string": "Applies inverse warp to the template labels to estimate label positions in target space (use for template-based segmentation)",
            "argstr": "-l",
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
            "help_string": "Type of transofmration model used for registration (EL = elastic transformation model, SY = SyN with time, arbitrary number of time points, S2 =  SyN with time optimized for 2 time points, GR = greedy SyN, EX = exponential, DD = diffeomorphic demons style exponential mapping, RI = purely rigid, RA = affine rigid",
            "argstr": "-t {transformation_model}",
        },
    ),
    (
        "out_prefix",
        str,
        "ants_",
        {
            "help_string": "Prefix that is prepended to all output files (default = ants_)",
            "argstr": "-o {out_prefix}",
        },
    ),
    (
        "quality_check",
        bool,
        {"help_string": "Perform a quality check of the result", "argstr": "-q 1"},
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
GenWarpFields_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("affine_transformation", File, {"help_string": "affine (prefix_Affine.txt)"}),
    ("warp_field", File, {"help_string": "warp field (prefix_Warp.nii)"}),
    (
        "inverse_warp_field",
        File,
        {"help_string": "inverse warp field (prefix_InverseWarp.nii)"},
    ),
    ("input_file", File, {"help_string": "input image (prefix_repaired.nii)"}),
    ("output_file", File, {"help_string": "output image (prefix_deformed.nii)"}),
]
GenWarpFields_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class GenWarpFields(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.legacy.gen_warp_fields import GenWarpFields

    """

    input_spec = GenWarpFields_input_spec
    output_spec = GenWarpFields_output_spec
    executable = "antsIntroduction.sh"
