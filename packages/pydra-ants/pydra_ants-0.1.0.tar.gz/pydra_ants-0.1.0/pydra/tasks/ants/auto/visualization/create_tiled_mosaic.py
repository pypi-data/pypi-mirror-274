from fileformats.application import Dicom
from fileformats.image import Bitmap, Jpeg, Png, Tiff
from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
import logging
from pydra.engine import ShellCommandTask, specs
import typing as ty


logger = logging.getLogger(__name__)


input_fields = [
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
            "help_string": "Main input is a 3-D grayscale image.",
            "argstr": "-i {input_image}",
            "mandatory": True,
        },
    ),
    (
        "rgb_image",
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
            "help_string": "An optional Rgb image can be added as an overlay.It must have the same imagegeometry as the input grayscale image.",
            "argstr": "-r {rgb_image}",
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
            "help_string": "Specifies the ROI of the RGB voxels used.",
            "argstr": "-x {mask_image}",
        },
    ),
    (
        "alpha_value",
        float,
        {
            "help_string": "If an Rgb image is provided, render the overlay using the specified alpha parameter.",
            "argstr": "-a {alpha_value:.2}",
        },
    ),
    (
        "output_image",
        str,
        "output.png",
        {
            "help_string": "The output consists of the tiled mosaic image.",
            "argstr": "-o {output_image}",
        },
    ),
    (
        "tile_geometry",
        str,
        {
            "help_string": 'The tile geometry specifies the number of rows and columnsin the output image. For example, if the user specifies "5x10", then 5 rows by 10 columns of slices are rendered. If R < 0 and C > 0 (or vice versa), the negative value is selectedbased on direction.',
            "argstr": "-t {tile_geometry}",
        },
    ),
    (
        "direction",
        int,
        {
            "help_string": "Specifies the direction of the slices. If no direction is specified, the direction with the coarsest spacing is chosen.",
            "argstr": "-d {direction}",
        },
    ),
    (
        "pad_or_crop",
        str,
        {
            "help_string": 'argument passed to -p flag:[padVoxelWidth,<constantValue=0>][lowerPadding[0]xlowerPadding[1],upperPadding[0]xupperPadding[1],constantValue]The user can specify whether to pad or crop a specified voxel-width boundary of each individual slice. For this program, cropping is simply padding with negative voxel-widths.If one pads (+), the user can also specify a constant pad value (default = 0). If a mask is specified, the user can use the mask to define the region, by using the keyword "mask" plus an offset, e.g. "-p mask+3".',
            "argstr": "-p {pad_or_crop}",
        },
    ),
    (
        "slices",
        str,
        {
            "help_string": "Number of slices to increment Slice1xSlice2xSlice3[numberOfSlicesToIncrement,<minSlice=0>,<maxSlice=lastSlice>]",
            "argstr": "-s {slices}",
        },
    ),
    ("flip_slice", str, {"help_string": "flipXxflipY", "argstr": "-f {flip_slice}"}),
    ("permute_axes", bool, {"help_string": "doPermute", "argstr": "-g"}),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
CreateTiledMosaic_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [("output_image", Png, {"help_string": "image file"})]
CreateTiledMosaic_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class CreateTiledMosaic(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.image import Bitmap, Jpeg, Png, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.visualization.create_tiled_mosaic import CreateTiledMosaic

    >>> task = CreateTiledMosaic()
    >>> task.inputs.input_image = "T1.nii.gz"
    >>> task.inputs.rgb_image = "rgb.nii.gz"
    >>> task.inputs.mask_image = "mask.nii.gz"
    >>> task.inputs.alpha_value = 0.5
    >>> task.inputs.output_image = "output.png"
    >>> task.inputs.direction = 2
    >>> task.inputs.pad_or_crop = "[ -15x -50 , -15x -30 ,0]"
    >>> task.inputs.slices = "[2 ,100 ,160]"
    >>> task.cmdline
    'CreateTiledMosaic -a 0.50 -d 2 -i T1.nii.gz -x mask.nii.gz -o output.png -p [ -15x -50 , -15x -30 ,0] -r rgb.nii.gz -s [2 ,100 ,160]'


    """

    input_spec = CreateTiledMosaic_input_spec
    output_spec = CreateTiledMosaic_output_spec
    executable = "CreateTiledMosaic"
