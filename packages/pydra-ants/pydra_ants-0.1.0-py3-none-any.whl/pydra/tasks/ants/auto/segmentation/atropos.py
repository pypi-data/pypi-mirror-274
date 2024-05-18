from fileformats.application import Dicom
from fileformats.generic import File
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
            "help_string": "image dimension (2, 3, or 4)",
            "argstr": "--image-dimensionality {dimension}",
        },
    ),
    (
        "intensity_images",
        ty.List[Nifti1],
        {
            "help_string": "",
            "argstr": "--intensity-image {intensity_images}...",
            "mandatory": True,
        },
    ),
    (
        "mask_image",
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
        {"help_string": "", "argstr": "--mask-image {mask_image}", "mandatory": True},
    ),
    (
        "initialization",
        ty.Any,
        {
            "help_string": "",
            "argstr": "{initialization}",
            "mandatory": True,
            "requires": ["number_of_tissue_classes"],
        },
    ),
    ("kmeans_init_centers", list, {"help_string": ""}),
    (
        "prior_image",
        ty.Any,
        {
            "help_string": "either a string pattern (e.g., 'prior%02d.nii') or an existing vector-image file."
        },
    ),
    ("number_of_tissue_classes", int, {"help_string": "", "mandatory": True}),
    ("prior_weighting", float, {"help_string": ""}),
    (
        "prior_probability_threshold",
        float,
        {"help_string": "", "requires": ["prior_weighting"]},
    ),
    (
        "likelihood_model",
        str,
        {"help_string": "", "argstr": "--likelihood-model {likelihood_model}"},
    ),
    (
        "mrf_smoothing_factor",
        float,
        {"help_string": "", "argstr": "{mrf_smoothing_factor}"},
    ),
    ("mrf_radius", list, {"help_string": "", "requires": ["mrf_smoothing_factor"]}),
    (
        "icm_use_synchronous_update",
        bool,
        {"help_string": "", "argstr": "{icm_use_synchronous_update}"},
    ),
    (
        "maximum_number_of_icm_terations",
        int,
        {"help_string": "", "requires": ["icm_use_synchronous_update"]},
    ),
    ("n_iterations", int, {"help_string": "", "argstr": "{n_iterations}"}),
    ("convergence_threshold", float, {"help_string": "", "requires": ["n_iterations"]}),
    (
        "posterior_formulation",
        str,
        {"help_string": "", "argstr": "{posterior_formulation}"},
    ),
    (
        "use_random_seed",
        bool,
        True,
        {
            "help_string": "use random seed value over constant",
            "argstr": "--use-random-seed {use_random_seed}",
        },
    ),
    (
        "use_mixture_model_proportions",
        bool,
        {"help_string": "", "requires": ["posterior_formulation"]},
    ),
    (
        "out_classified_image_name",
        Path,
        {"help_string": "", "argstr": "{out_classified_image_name}"},
    ),
    ("save_posteriors", bool, {"help_string": ""}),
    (
        "output_posteriors_name_template",
        str,
        "POSTERIOR_%02d.nii.gz",
        {"help_string": ""},
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
Atropos_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "classified_image",
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
        {},
    ),
    ("posteriors", ty.List[File], {}),
]
Atropos_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Atropos(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.atropos import Atropos

    >>> task = Atropos()
    >>> task.inputs.dimension = 3
    >>> task.inputs.intensity_images = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.mask_image = "mask.nii"
    >>> task.inputs.initialization = "Random"
    >>> task.inputs.number_of_tissue_classes = 2
    >>> task.inputs.likelihood_model = "Gaussian"
    >>> task.inputs.mrf_smoothing_factor = 0.2
    >>> task.inputs.mrf_radius = [1, 1, 1]
    >>> task.inputs.icm_use_synchronous_update = True
    >>> task.inputs.maximum_number_of_icm_terations = 1
    >>> task.inputs.n_iterations = 5
    >>> task.inputs.convergence_threshold = 0.000001
    >>> task.inputs.posterior_formulation = "Socrates"
    >>> task.inputs.use_mixture_model_proportions = True
    >>> task.inputs.save_posteriors = True
    >>> task.cmdline
    'Atropos --image-dimensionality 3 --icm [1,1] --initialization Random[2] --intensity-image structural.nii --likelihood-model Gaussian --mask-image mask.nii --mrf [0.2,1x1x1] --convergence [5,1e-06] --output [structural_labeled.nii,POSTERIOR_%02d.nii.gz] --posterior-formulation Socrates[1] --use-random-seed 1'


    >>> task = Atropos()
    >>> task.inputs.dimension = 3
    >>> task.inputs.intensity_images = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.mask_image = "mask.nii"
    >>> task.inputs.initialization = "KMeans"
    >>> task.inputs.kmeans_init_centers = [100, 200]
    >>> task.inputs.number_of_tissue_classes = 2
    >>> task.inputs.likelihood_model = "Gaussian"
    >>> task.inputs.mrf_smoothing_factor = 0.2
    >>> task.inputs.mrf_radius = [1, 1, 1]
    >>> task.inputs.icm_use_synchronous_update = True
    >>> task.inputs.maximum_number_of_icm_terations = 1
    >>> task.inputs.n_iterations = 5
    >>> task.inputs.convergence_threshold = 0.000001
    >>> task.inputs.posterior_formulation = "Socrates"
    >>> task.inputs.use_mixture_model_proportions = True
    >>> task.inputs.save_posteriors = True
    >>> task.cmdline
    'Atropos --image-dimensionality 3 --icm [1,1] --initialization KMeans[2,100,200] --intensity-image structural.nii --likelihood-model Gaussian --mask-image mask.nii --mrf [0.2,1x1x1] --convergence [5,1e-06] --output [structural_labeled.nii,POSTERIOR_%02d.nii.gz] --posterior-formulation Socrates[1] --use-random-seed 1'


    >>> task = Atropos()
    >>> task.inputs.dimension = 3
    >>> task.inputs.intensity_images = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.mask_image = "mask.nii"
    >>> task.inputs.initialization = "PriorProbabilityImages"
    >>> task.inputs.prior_image = "BrainSegmentationPrior%02d.nii.gz"
    >>> task.inputs.number_of_tissue_classes = 2
    >>> task.inputs.prior_weighting = 0.8
    >>> task.inputs.prior_probability_threshold = 0.0000001
    >>> task.inputs.likelihood_model = "Gaussian"
    >>> task.inputs.mrf_smoothing_factor = 0.2
    >>> task.inputs.mrf_radius = [1, 1, 1]
    >>> task.inputs.icm_use_synchronous_update = True
    >>> task.inputs.maximum_number_of_icm_terations = 1
    >>> task.inputs.n_iterations = 5
    >>> task.inputs.convergence_threshold = 0.000001
    >>> task.inputs.posterior_formulation = "Socrates"
    >>> task.inputs.use_mixture_model_proportions = True
    >>> task.inputs.save_posteriors = True
    >>> task.cmdline
    'Atropos --image-dimensionality 3 --icm [1,1] --initialization PriorProbabilityImages[2,BrainSegmentationPrior%02d.nii.gz,0.8,1e-07] --intensity-image structural.nii --likelihood-model Gaussian --mask-image mask.nii --mrf [0.2,1x1x1] --convergence [5,1e-06] --output [structural_labeled.nii,POSTERIOR_%02d.nii.gz] --posterior-formulation Socrates[1] --use-random-seed 1'


    >>> task = Atropos()
    >>> task.inputs.dimension = 3
    >>> task.inputs.intensity_images = [Nifti1.mock("s"), Nifti1.mock("t"), Nifti1.mock("r"), Nifti1.mock("u"), Nifti1.mock("c"), Nifti1.mock("t"), Nifti1.mock("u"), Nifti1.mock("r"), Nifti1.mock("a"), Nifti1.mock("l"), Nifti1.mock("."), Nifti1.mock("n"), Nifti1.mock("i"), Nifti1.mock("i")]
    >>> task.inputs.mask_image = "mask.nii"
    >>> task.inputs.initialization = "PriorLabelImage"
    >>> task.inputs.prior_image = "segmentation0.nii.gz"
    >>> task.inputs.number_of_tissue_classes = 2
    >>> task.inputs.prior_weighting = 0.8
    >>> task.inputs.likelihood_model = "Gaussian"
    >>> task.inputs.mrf_smoothing_factor = 0.2
    >>> task.inputs.mrf_radius = [1, 1, 1]
    >>> task.inputs.icm_use_synchronous_update = True
    >>> task.inputs.maximum_number_of_icm_terations = 1
    >>> task.inputs.n_iterations = 5
    >>> task.inputs.convergence_threshold = 0.000001
    >>> task.inputs.posterior_formulation = "Socrates"
    >>> task.inputs.use_mixture_model_proportions = True
    >>> task.inputs.save_posteriors = True
    >>> task.cmdline
    'Atropos --image-dimensionality 3 --icm [1,1] --initialization PriorLabelImage[2,segmentation0.nii.gz,0.8] --intensity-image structural.nii --likelihood-model Gaussian --mask-image mask.nii --mrf [0.2,1x1x1] --convergence [5,1e-06] --output [structural_labeled.nii,POSTERIOR_%02d.nii.gz] --posterior-formulation Socrates[1] --use-random-seed 1'


    """

    input_spec = Atropos_input_spec
    output_spec = Atropos_output_spec
    executable = "Atropos"
