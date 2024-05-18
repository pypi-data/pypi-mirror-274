from fileformats.application import Dicom
from fileformats.image import Bitmap, Jpeg, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
from fileformats.text import TextFile
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
            "help_string": "image dimension (2 or 3)",
            "argstr": "{dimension}",
            "position": 1,
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
            "help_string": "image to apply transformation to (generally a coregistered functional)",
            "argstr": "{input_image}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "output_image",
        Path,
        {
            "help_string": "name of the output warped image",
            "argstr": "{output_image}",
            "position": 3,
            "xor": ["out_postfix"],
            "output_file_template": "output_image",
        },
    ),
    (
        "out_postfix",
        str,
        "_wimt",
        {
            "help_string": "Postfix that is prepended to all output files (default = _wimt)",
            "xor": ["output_image"],
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
            "help_string": "reference image space that you wish to warp INTO",
            "argstr": "-R {reference_image}",
            "xor": ["tightest_box"],
        },
    ),
    (
        "tightest_box",
        bool,
        {
            "help_string": "computes tightest bounding box (overridden by reference_image if given)",
            "argstr": "--tightest-bounding-box",
            "xor": ["reference_image"],
        },
    ),
    (
        "reslice_by_header",
        bool,
        {
            "help_string": "Uses orientation matrix and origin encoded in reference image file header. Not typically used with additional transforms",
            "argstr": "--reslice-by-header",
        },
    ),
    (
        "use_nearest",
        bool,
        {"help_string": "Use nearest neighbor interpolation", "argstr": "--use-NN"},
    ),
    (
        "use_bspline",
        bool,
        {
            "help_string": "Use 3rd order B-Spline interpolation",
            "argstr": "--use-BSpline",
        },
    ),
    (
        "transformation_series",
        ty.List[ty.Union[TextFile, NiftiGz]],
        {
            "help_string": "transformation file(s) to be applied",
            "argstr": "{transformation_series}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "invert_affine",
        list,
        {
            "help_string": 'List of Affine transformations to invert.E.g.: [1,4,5] inverts the 1st, 4th, and 5th Affines found in transformation_series. Note that indexing starts with 1 and does not include warp fields. Affine transformations are distinguished from warp fields by the word "affine" included in their filenames.'
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
WarpImageMultiTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
WarpImageMultiTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class WarpImageMultiTransform(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.ants.auto.resampling.warp_image_multi_transform import WarpImageMultiTransform

    >>> task = WarpImageMultiTransform()
    >>> task.inputs.input_image = "structural.nii"
    >>> task.inputs.reference_image = "ants_deformed.nii.gz"
    >>> task.inputs.transformation_series = ["ants_Warp.nii.gz","ants_Affine.txt"]
    >>> task.cmdline
    'WarpImageMultiTransform 3 structural.nii structural_wimt.nii -R ants_deformed.nii.gz ants_Warp.nii.gz ants_Affine.txt'


    >>> task = WarpImageMultiTransform()
    >>> task.inputs.input_image = "diffusion_weighted.nii"
    >>> task.inputs.reference_image = "functional.nii"
    >>> task.inputs.transformation_series = ["func2anat_coreg_Affine.txt","func2anat_InverseWarp.nii.gz",     "dwi2anat_Warp.nii.gz","dwi2anat_coreg_Affine.txt"]
    >>> task.inputs.invert_affine = [1]  # this will invert the 1st Affine file: "func2anat_coreg_Affine.txt"
    >>> task.cmdline
    'WarpImageMultiTransform 3 diffusion_weighted.nii diffusion_weighted_wimt.nii -R functional.nii -i func2anat_coreg_Affine.txt func2anat_InverseWarp.nii.gz dwi2anat_Warp.nii.gz dwi2anat_coreg_Affine.txt'


    """

    input_spec = WarpImageMultiTransform_input_spec
    output_spec = WarpImageMultiTransform_output_spec
    executable = "WarpImageMultiTransform"
