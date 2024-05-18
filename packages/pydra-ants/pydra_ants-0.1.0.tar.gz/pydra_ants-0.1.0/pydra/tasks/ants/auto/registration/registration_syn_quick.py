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
        {"help_string": "image dimension (2 or 3)", "argstr": "-d {dimension}"},
    ),
    (
        "fixed_image",
        ty.List[
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
            ]
        ],
        {
            "help_string": "Fixed image or source image or reference image",
            "argstr": "-f {fixed_image}...",
            "mandatory": True,
        },
    ),
    (
        "moving_image",
        ty.List[
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
            ]
        ],
        {
            "help_string": "Moving image or target image",
            "argstr": "-m {moving_image}...",
            "mandatory": True,
        },
    ),
    (
        "output_prefix",
        str,
        "transform",
        {
            "help_string": "A prefix that is prepended to all output files",
            "argstr": "-o {output_prefix}",
        },
    ),
    (
        "num_threads",
        int,
        1,
        {
            "help_string": "Number of threads (default = 1)",
            "argstr": "-n {num_threads}",
        },
    ),
    (
        "transform_type",
        ty.Any,
        "s",
        {
            "help_string": "Transform type\n\n  * t:  translation\n  * r:  rigid\n  * a:  rigid + affine\n  * s:  rigid + affine + deformable syn (default)\n  * sr: rigid + deformable syn\n  * b:  rigid + affine + deformable b-spline syn\n  * br: rigid + deformable b-spline syn\n\n",
            "argstr": "-t {transform_type}",
        },
    ),
    (
        "use_histogram_matching",
        bool,
        {
            "help_string": "use histogram matching",
            "argstr": "-j {use_histogram_matching}",
        },
    ),
    (
        "histogram_bins",
        int,
        32,
        {
            "help_string": "histogram bins for mutual information in SyN stage                                  (default = 32)",
            "argstr": "-r {histogram_bins}",
        },
    ),
    (
        "spline_distance",
        int,
        26,
        {
            "help_string": "spline distance for deformable B-spline SyN transform                                  (default = 26)",
            "argstr": "-s {spline_distance}",
        },
    ),
    (
        "precision_type",
        ty.Any,
        "double",
        {
            "help_string": "precision type (default = double)",
            "argstr": "-p {precision_type}",
        },
    ),
    (
        "random_seed",
        int,
        {"help_string": "fixed random seed", "argstr": "-e {random_seed}"},
    ),
]
RegistrationSynQuick_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "warped_image",
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
        {"help_string": "Warped image"},
    ),
    (
        "inverse_warped_image",
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
        {"help_string": "Inverse warped image"},
    ),
    ("out_matrix", File, {"help_string": "Affine matrix"}),
    ("forward_warp_field", File, {"help_string": "Forward warp field"}),
    ("inverse_warp_field", File, {"help_string": "Inverse warp field"}),
]
RegistrationSynQuick_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class RegistrationSynQuick(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.registration.registration_syn_quick import RegistrationSynQuick

    >>> task = RegistrationSynQuick()
    >>> task.inputs.fixed_image = "fixed1.nii"
    >>> task.inputs.moving_image = "moving1.nii"
    >>> task.inputs.num_threads = 2
    >>> task.cmdline
    'antsRegistrationSyNQuick.sh -d 3 -f fixed1.nii -r 32 -m moving1.nii -n 2 -o transform -p d -s 26 -t s'


    >>> task = RegistrationSynQuick()
    >>> task.inputs.fixed_image = ["fixed1.nii", "fixed2.nii"]
    >>> task.inputs.moving_image = ["moving1.nii", "moving2.nii"]
    >>> task.inputs.num_threads = 2
    >>> task.cmdline
    'antsRegistrationSyNQuick.sh -d 3 -f fixed1.nii -f fixed2.nii -r 32 -m moving1.nii -m moving2.nii -n 2 -o transform -p d -s 26 -t s'


    """

    input_spec = RegistrationSynQuick_input_spec
    output_spec = RegistrationSynQuick_output_spec
    executable = "antsRegistrationSyNQuick.sh"
