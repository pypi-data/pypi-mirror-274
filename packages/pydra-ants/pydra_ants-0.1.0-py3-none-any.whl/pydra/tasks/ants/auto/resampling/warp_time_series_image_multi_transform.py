from fileformats.application import Dicom
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
        4,
        {
            "help_string": "image dimension (3 or 4)",
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
            "copyfile": True,
            "mandatory": True,
        },
    ),
    (
        "out_postfix",
        str,
        "_wtsimt",
        {
            "help_string": "Postfix that is prepended to all output files (default = _wtsimt)",
            "argstr": "{out_postfix}",
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
            "argstr": "--use-Bspline",
        },
    ),
    (
        "transformation_series",
        ty.List[NiftiGz],
        {
            "help_string": "transformation file(s) to be applied",
            "argstr": "{transformation_series}",
            "copyfile": False,
            "mandatory": True,
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
WarpTimeSeriesImageMultiTransform_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "output_image",
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
    )
]
WarpTimeSeriesImageMultiTransform_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class WarpTimeSeriesImageMultiTransform(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.resampling.warp_time_series_image_multi_transform import WarpTimeSeriesImageMultiTransform

    >>> task = WarpTimeSeriesImageMultiTransform()
    >>> task.inputs.input_image = "resting.nii"
    >>> task.inputs.reference_image = "ants_deformed.nii.gz"
    >>> task.inputs.transformation_series = [NiftiGz.mock("ants_Warp.nii.gz"), NiftiGz.mock("ants_Affine.txt")]
    >>> task.cmdline
    'WarpTimeSeriesImageMultiTransform 4 resting.nii resting_wtsimt.nii -R ants_deformed.nii.gz ants_Warp.nii.gz ants_Affine.txt'


    >>> task = WarpTimeSeriesImageMultiTransform()
    >>> task.inputs.input_image = "resting.nii"
    >>> task.inputs.reference_image = "ants_deformed.nii.gz"
    >>> task.inputs.transformation_series = [NiftiGz.mock("ants_Warp.nii.gz"), NiftiGz.mock("ants_Affine.txt")]
    >>> task.inputs.invert_affine = [1] # # this will invert the 1st Affine file: ants_Affine.txt
    >>> task.cmdline
    'WarpTimeSeriesImageMultiTransform 4 resting.nii resting_wtsimt.nii -R ants_deformed.nii.gz ants_Warp.nii.gz -i ants_Affine.txt'


    """

    input_spec = WarpTimeSeriesImageMultiTransform_input_spec
    output_spec = WarpTimeSeriesImageMultiTransform_output_spec
    executable = "WarpTimeSeriesImageMultiTransform"
