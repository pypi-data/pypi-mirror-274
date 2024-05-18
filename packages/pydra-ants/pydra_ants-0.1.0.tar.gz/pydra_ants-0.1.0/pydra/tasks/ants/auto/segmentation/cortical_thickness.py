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
            "help_string": "Structural *intensity* image, typically T1. If more than one anatomical image is specified, subsequently specified images are used during the segmentation process. However, only the first image is used in the registration of priors. Our suggestion would be to specify the T1 as the first image.",
            "argstr": "-a {anatomical_image}",
            "mandatory": True,
        },
    ),
    (
        "brain_template",
        NiftiGz,
        {
            "help_string": "Anatomical *intensity* template (possibly created using a population data set with buildtemplateparallel.sh in ANTs). This template is  *not* skull-stripped.",
            "argstr": "-e {brain_template}",
            "mandatory": True,
        },
    ),
    (
        "brain_probability_mask",
        NiftiGz,
        {
            "help_string": "brain probability mask in template space",
            "argstr": "-m {brain_probability_mask}",
            "copyfile": False,
            "mandatory": True,
        },
    ),
    (
        "segmentation_priors",
        ty.List[NiftiGz],
        {"help_string": "", "argstr": "-p {segmentation_priors}", "mandatory": True},
    ),
    (
        "out_prefix",
        str,
        "antsCT_",
        {
            "help_string": "Prefix that is prepended to all output files",
            "argstr": "-o {out_prefix}",
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
        "t1_registration_template",
        NiftiGz,
        {
            "help_string": "Anatomical *intensity* template (assumed to be skull-stripped). A common case would be where this would be the same template as specified in the -e option which is not skull stripped.",
            "argstr": "-t {t1_registration_template}",
            "mandatory": True,
        },
    ),
    (
        "extraction_registration_mask",
        File,
        {
            "help_string": "Mask (defined in the template space) used during registration for brain extraction.",
            "argstr": "-f {extraction_registration_mask}",
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
        "max_iterations",
        int,
        {
            "help_string": "ANTS registration max iterations (default = 100x100x70x20)",
            "argstr": "-i {max_iterations}",
        },
    ),
    (
        "prior_segmentation_weight",
        float,
        {
            "help_string": "Atropos spatial prior *probability* weight for the segmentation",
            "argstr": "-w {prior_segmentation_weight}",
        },
    ),
    (
        "segmentation_iterations",
        int,
        {
            "help_string": "N4 -> Atropos -> N4 iterations during segmentation (default = 3)",
            "argstr": "-n {segmentation_iterations}",
        },
    ),
    (
        "posterior_formulation",
        str,
        {
            "help_string": "Atropos posterior formulation and whether or not to use mixture model proportions. e.g 'Socrates[1]' (default) or 'Aristotle[1]'. Choose the latter if you want use the distance priors (see also the -l option for label propagation control).",
            "argstr": "-b {posterior_formulation}",
        },
    ),
    (
        "use_floatingpoint_precision",
        ty.Any,
        {
            "help_string": "Use floating point precision in registrations (default = 0)",
            "argstr": "-j {use_floatingpoint_precision}",
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
        "b_spline_smoothing",
        bool,
        {
            "help_string": "Use B-spline SyN for registrations and B-spline exponential mapping in DiReCT.",
            "argstr": "-v",
        },
    ),
    (
        "cortical_label_image",
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
        {"help_string": "Cortical ROI labels to use as a prior for ATITH."},
    ),
    (
        "label_propagation",
        str,
        {
            "help_string": "Incorporate a distance prior one the posterior formulation.  Should be of the form 'label[lambda,boundaryProbability]' where label is a value of 1,2,3,... denoting label ID.  The label probability for anything outside the current label = boundaryProbability * exp( -lambda * distanceFromBoundary ) Intuitively, smaller lambda values will increase the spatial capture range of the distance prior.  To apply to all label values, simply omit specifying the label, i.e. -l [lambda,boundaryProbability].",
            "argstr": "-l {label_propagation}",
        },
    ),
    (
        "quick_registration",
        bool,
        {
            "help_string": "If = 1, use antsRegistrationSyNQuick.sh as the basis for registration during brain extraction, brain segmentation, and (optional) normalization to a template. Otherwise use antsRegistrationSyN.sh (default = 0).",
            "argstr": "-q 1",
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
CorticalThickness_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("BrainExtractionMask", File, {"help_string": "brain extraction mask"}),
    ("ExtractedBrainN4", File, {"help_string": "extracted brain from N4 image"}),
    ("BrainSegmentation", File, {"help_string": "brain segmentation image"}),
    ("BrainSegmentationN4", File, {"help_string": "N4 corrected image"}),
    (
        "BrainSegmentationPosteriors",
        ty.List[File],
        {"help_string": "Posterior probability images"},
    ),
    ("CorticalThickness", File, {"help_string": "cortical thickness file"}),
    (
        "TemplateToSubject1GenericAffine",
        File,
        {"help_string": "Template to subject affine"},
    ),
    ("TemplateToSubject0Warp", File, {"help_string": "Template to subject warp"}),
    (
        "SubjectToTemplate1Warp",
        File,
        {"help_string": "Template to subject inverse warp"},
    ),
    (
        "SubjectToTemplate0GenericAffine",
        File,
        {"help_string": "Template to subject inverse affine"},
    ),
    (
        "SubjectToTemplateLogJacobian",
        File,
        {"help_string": "Template to subject log jacobian"},
    ),
    (
        "CorticalThicknessNormedToTemplate",
        File,
        {"help_string": "Normalized cortical thickness"},
    ),
    ("BrainVolumes", File, {"help_string": "Brain volumes as text"}),
]
CorticalThickness_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CorticalThickness(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.cortical_thickness import CorticalThickness

    >>> task = CorticalThickness()
    >>> task.inputs.dimension = 3
    >>> task.inputs.anatomical_image = "T1.nii.gz"
    >>> task.inputs.brain_template = NiftiGz.mock("study_template.nii.gz")
    >>> task.inputs.brain_probability_mask = NiftiGz.mock("ProbabilityMaskOfStudyTemplate.nii.gz")
    >>> task.inputs.segmentation_priors = [NiftiGz.mock("BrainSegmentationPrior01.nii.gz"), NiftiGz.mock("BrainSegmentationPrior02.nii.gz"), NiftiGz.mock("BrainSegmentationPrior03.nii.gz"), NiftiGz.mock("BrainSegmentationPrior04.nii.gz")]
    >>> task.inputs.t1_registration_template = NiftiGz.mock("brain_study_template.nii.gz")
    >>> task.inputs.extraction_registration_mask = File.mock()
    >>> task.cmdline
    'antsCorticalThickness.sh -a T1.nii.gz -m ProbabilityMaskOfStudyTemplate.nii.gz -e study_template.nii.gz -d 3 -s nii.gz -o antsCT_ -p nipype_priors/BrainSegmentationPrior%02d.nii.gz -t brain_study_template.nii.gz'


    """

    input_spec = CorticalThickness_input_spec
    output_spec = CorticalThickness_output_spec
    executable = "antsCorticalThickness.sh"
