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
        "anatomical_image",
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
            "help_string": "Structural image, typically T1.  If more than one anatomical image is specified, subsequently specified images are used during the segmentation process.  However, only the first image is used in the registration of priors. Our suggestion would be to specify the T1 as the first image. Anatomical template created using e.g. LPBA40 data set with buildtemplateparallel.sh in ANTs.",
            "argstr": "-a {anatomical_image}",
            "mandatory": True,
        },
    ),
    (
        "brain_template",
        NiftiGz,
        {
            "help_string": "Anatomical template created using e.g. LPBA40 data set with buildtemplateparallel.sh in ANTs.",
            "argstr": "-e {brain_template}",
            "mandatory": True,
        },
    ),
    (
        "brain_probability_mask",
        NiftiGz,
        {
            "help_string": "Brain probability mask created using e.g. LPBA40 data set which have brain masks defined, and warped to anatomical template and averaged resulting in a probability image.",
            "argstr": "-m {brain_probability_mask}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "out_prefix",
        str,
        "highres001_",
        {
            "help_string": "Prefix that is prepended to all output files",
            "argstr": "-o {out_prefix}",
        },
    ),
    (
        "extraction_registration_mask",
        File,
        {
            "help_string": "Mask (defined in the template space) used during registration for brain extraction. To limit the metric computation to a specific region.",
            "argstr": "-f {extraction_registration_mask}",
        },
    ),
    (
        "image_suffix",
        str,
        "nii.gz",
        {
            "help_string": "any of standard ITK formats, nii.gz is default",
            "argstr": "-s {image_suffix}",
        },
    ),
    (
        "use_random_seeding",
        ty.Any,
        {
            "help_string": "Use random number generated from system clock in Atropos (default = 1)",
            "argstr": "-u {use_random_seeding}",
        },
    ),
    (
        "keep_temporary_files",
        int,
        {
            "help_string": "Keep brain extraction/segmentation warps, etc (default = 0).",
            "argstr": "-k {keep_temporary_files}",
        },
    ),
    (
        "use_floatingpoint_precision",
        ty.Any,
        {
            "help_string": "Use floating point precision in registrations (default = 0)",
            "argstr": "-q {use_floatingpoint_precision}",
        },
    ),
    (
        "debug",
        bool,
        {
            "help_string": "If > 0, runs a faster version of the script. Only for testing. Implies -u 0. Requires single thread computation for complete reproducibility.",
            "argstr": "-z 1",
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
BrainExtraction_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("BrainExtractionMask", File, {"help_string": "brain extraction mask"}),
    ("BrainExtractionBrain", File, {"help_string": "brain extraction image"}),
    ("BrainExtractionCSF", File, {"help_string": "segmentation mask with only CSF"}),
    (
        "BrainExtractionGM",
        File,
        {"help_string": "segmentation mask with only grey matter"},
    ),
    ("BrainExtractionInitialAffine", File, {}),
    ("BrainExtractionInitialAffineFixed", File, {}),
    ("BrainExtractionInitialAffineMoving", File, {}),
    ("BrainExtractionLaplacian", File, {}),
    ("BrainExtractionPrior0GenericAffine", File, {}),
    ("BrainExtractionPrior1InverseWarp", File, {}),
    ("BrainExtractionPrior1Warp", File, {}),
    ("BrainExtractionPriorWarped", File, {}),
    (
        "BrainExtractionSegmentation",
        File,
        {"help_string": "segmentation mask with CSF, GM, and WM"},
    ),
    ("BrainExtractionTemplateLaplacian", File, {}),
    ("BrainExtractionTmp", File, {}),
    (
        "BrainExtractionWM",
        File,
        {"help_string": "segmenration mask with only white matter"},
    ),
    ("N4Corrected0", File, {"help_string": "N4 bias field corrected image"}),
    ("N4Truncated0", File, {}),
]
BrainExtraction_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class BrainExtraction(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.brain_extraction import BrainExtraction

    >>> task = BrainExtraction()
    >>> task.inputs.dimension = 3
    >>> task.inputs.anatomical_image = "T1.nii.gz"
    >>> task.inputs.brain_template = NiftiGz.mock("study_template.nii.gz")
    >>> task.inputs.brain_probability_mask = NiftiGz.mock("ProbabilityMaskOfStudyTemplate.nii.gz")
    >>> task.inputs.extraction_registration_mask = File.mock()
    >>> task.cmdline
    'antsBrainExtraction.sh -a T1.nii.gz -m ProbabilityMaskOfStudyTemplate.nii.gz -e study_template.nii.gz -d 3 -s nii.gz -o highres001_'


    """

    input_spec = BrainExtraction_input_spec
    output_spec = BrainExtraction_output_spec
    executable = "antsBrainExtraction.sh"
