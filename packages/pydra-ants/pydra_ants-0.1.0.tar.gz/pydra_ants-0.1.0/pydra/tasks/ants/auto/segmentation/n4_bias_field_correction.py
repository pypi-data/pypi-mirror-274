from fileformats.application import Dicom
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
        {"help_string": "image dimension (2, 3 or 4)", "argstr": "-d {dimension}"},
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
            "help_string": "input for bias correction. Negative values or values close to zero should be processed prior to correction",
            "argstr": "--input-image {input_image}",
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
        {
            "help_string": "image to specify region to perform final bias correction in",
            "argstr": "--mask-image {mask_image}",
        },
    ),
    (
        "weight_image",
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
            "help_string": "image for relative weighting (e.g. probability map of the white matter) of voxels during the B-spline fitting. ",
            "argstr": "--weight-image {weight_image}",
        },
    ),
    (
        "output_image",
        str,
        {
            "help_string": "output file name",
            "argstr": "--output {output_image}",
            "output_file_template": "{input_image}_corrected",
        },
    ),
    (
        "bspline_fitting_distance",
        float,
        {"help_string": "", "argstr": "--bspline-fitting {bspline_fitting_distance}"},
    ),
    (
        "bspline_order",
        int,
        {"help_string": "", "requires": ["bspline_fitting_distance"]},
    ),
    (
        "shrink_factor",
        int,
        {"help_string": "", "argstr": "--shrink-factor {shrink_factor}"},
    ),
    (
        "n_iterations",
        list,
        {"help_string": "", "argstr": "--convergence {n_iterations}"},
    ),
    ("convergence_threshold", float, {"help_string": "", "requires": ["n_iterations"]}),
    (
        "save_bias",
        bool,
        {
            "help_string": "True if the estimated bias should be saved to file.",
            "mandatory": True,
            "xor": ["bias_image"],
        },
    ),
    ("bias_image", Path, {"help_string": "Filename for the estimated bias."}),
    (
        "copy_header",
        bool,
        {
            "help_string": "copy headers of the original image into the output (corrected) file",
            "mandatory": True,
        },
    ),
    (
        "rescale_intensities",
        bool,
        False,
        {
            "help_string": '[NOTE: Only ANTs>=2.1.0]\nAt each iteration, a new intensity mapping is calculated and applied but there\nis nothing which constrains the new intensity range to be within certain values.\nThe result is that the range can "drift" from the original at each iteration.\nThis option rescales to the [min,max] range of the original image intensities\nwithin the user-specified mask.',
            "argstr": "-r",
        },
    ),
    (
        "histogram_sharpening",
        ty.Any,
        {
            "help_string": "Three-values tuple of histogram sharpening parameters (FWHM, wienerNose, numberOfHistogramBins).\nThese options describe the histogram sharpening parameters, i.e. the deconvolution step parameters described in the original N3 algorithm.\nThe default values have been shown to work fairly well.",
            "argstr": "--histogram-sharpening [{histogram_sharpening[0]},{histogram_sharpening[1]},{histogram_sharpening[2]}]",
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
N4BiasFieldCorrection_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "bias_image",
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
        {"help_string": "Estimated bias"},
    )
]
N4BiasFieldCorrection_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class N4BiasFieldCorrection(ShellCommandTask):
    """
    Examples
    -------

    >>> import copy
    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.n4_bias_field_correction import N4BiasFieldCorrection

    >>> task = N4BiasFieldCorrection()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.bspline_fitting_distance = 300
    >>> task.inputs.shrink_factor = 3
    >>> task.inputs.n_iterations = [50,50,30,20]
    >>> task.cmdline
    'N4BiasFieldCorrection --bspline-fitting [ 300 ] -d 3 --input-image structural.nii --convergence [ 50x50x30x20 ] --output structural_corrected.nii --shrink-factor 3'


    >>> task = N4BiasFieldCorrection()
    >>> task.inputs.convergence_threshold = 1e-6
    >>> task.cmdline
    'N4BiasFieldCorrection --bspline-fitting [ 300 ] -d 3 --input-image structural.nii --convergence [ 50x50x30x20, 1e-06 ] --output structural_corrected.nii --shrink-factor 3'


    >>> task = N4BiasFieldCorrection()
    >>> task.inputs.bspline_order = 5
    >>> task.cmdline
    'N4BiasFieldCorrection --bspline-fitting [ 300, 5 ] -d 3 --input-image structural.nii --convergence [ 50x50x30x20, 1e-06 ] --output structural_corrected.nii --shrink-factor 3'


    >>> task = N4BiasFieldCorrection()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.save_bias = True
    >>> task.cmdline
    'N4BiasFieldCorrection -d 3 --input-image structural.nii --output [ structural_corrected.nii, structural_bias.nii ]'


    >>> task = N4BiasFieldCorrection()
    >>> task.inputs.dimension = 3
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.histogram_sharpening = (0.12, 0.02, 200)
    >>> task.cmdline
    'N4BiasFieldCorrection -d 3 --histogram-sharpening [0.12,0.02,200] --input-image structural.nii --output structural_corrected.nii'


    """

    input_spec = N4BiasFieldCorrection_input_spec
    output_spec = N4BiasFieldCorrection_output_spec
    executable = "N4BiasFieldCorrection"
