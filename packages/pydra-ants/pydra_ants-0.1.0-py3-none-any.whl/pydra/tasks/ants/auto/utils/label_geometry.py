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
        3,
        {
            "help_string": "image dimension (2 or 3)",
            "argstr": "{dimension}",
            "position": 0,
        },
    ),
    (
        "label_image",
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
            "help_string": "label image to use for extracting geometry measures",
            "argstr": "{label_image}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "intensity_image",
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
            "help_string": "Intensity image to extract values from. This is an optional input",
            "argstr": "{intensity_image}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "output_file",
        str,
        {
            "help_string": "name of output file",
            "argstr": "{output_file}",
            "position": 3,
            "output_file_template": "{label_image}.csv",
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
LabelGeometry_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
LabelGeometry_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class LabelGeometry(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.utils.label_geometry import LabelGeometry

    >>> task = LabelGeometry()
    >>> task.inputs.dimension = 3
    >>> task.inputs.label_image = "atlas.nii.gz"
    >>> task.cmdline
    'LabelGeometryMeasures 3 atlas.nii.gz [] atlas.csv'


    >>> task = LabelGeometry()
    >>> task.inputs.intensity_image = "ants_Warp.nii.gz"
    >>> task.cmdline
    'LabelGeometryMeasures 3 atlas.nii.gz ants_Warp.nii.gz atlas.csv'


    """

    input_spec = LabelGeometry_input_spec
    output_spec = LabelGeometry_output_spec
    executable = "LabelGeometryMeasures"
