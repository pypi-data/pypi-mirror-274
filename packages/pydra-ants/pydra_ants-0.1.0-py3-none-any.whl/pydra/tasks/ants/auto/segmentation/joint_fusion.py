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
        {
            "help_string": "This option forces the image to be treated as a specified-dimensional image. If not specified, the program tries to infer the dimensionality from the input image.",
            "argstr": "-d {dimension}",
        },
    ),
    (
        "target_image",
        list,
        {
            "help_string": "The target image (or multimodal target images) assumed to be aligned to a common image domain.",
            "argstr": "-t {target_image}",
            "mandatory": True,
        },
    ),
    (
        "atlas_image",
        list,
        {
            "help_string": "The atlas image (or multimodal atlas images) assumed to be aligned to a common image domain.",
            "argstr": "-g {atlas_image}...",
            "mandatory": True,
        },
    ),
    (
        "atlas_segmentation_image",
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
            "help_string": "The atlas segmentation images. For performing label fusion the number of specified segmentations should be identical to the number of atlas image sets.",
            "argstr": "-l {atlas_segmentation_image}...",
            "mandatory": True,
        },
    ),
    (
        "alpha",
        float,
        0.1,
        {
            "help_string": "Regularization term added to matrix Mx for calculating the inverse. Default = 0.1",
            "argstr": "-a {alpha}",
        },
    ),
    (
        "beta",
        float,
        2.0,
        {
            "help_string": "Exponent for mapping intensity difference to the joint error. Default = 2.0",
            "argstr": "-b {beta}",
        },
    ),
    (
        "retain_label_posterior_images",
        bool,
        False,
        {
            "help_string": "Retain label posterior probability images. Requires atlas segmentations to be specified. Default = false",
            "argstr": "-r",
            "requires": ["atlas_segmentation_image"],
        },
    ),
    (
        "retain_atlas_voting_images",
        bool,
        False,
        {"help_string": "Retain atlas voting images. Default = false", "argstr": "-f"},
    ),
    (
        "constrain_nonnegative",
        bool,
        False,
        {"help_string": "Constrain solution to non-negative weights.", "argstr": "-c"},
    ),
    (
        "patch_radius",
        list,
        {
            "help_string": "Patch radius for similarity measures. Default: 2x2x2",
            "argstr": "-p {patch_radius}",
        },
    ),
    (
        "patch_metric",
        ty.Any,
        {
            "help_string": "Metric to be used in determining the most similar neighborhood patch. Options include Pearson's correlation (PC) and mean squares (MSQ). Default = PC (Pearson correlation).",
            "argstr": "-m {patch_metric}",
        },
    ),
    (
        "search_radius",
        list,
        [3, 3, 3],
        {
            "help_string": "Search radius for similarity measures. Default = 3x3x3. One can also specify an image where the value at the voxel specifies the isotropic search radius at that voxel.",
            "argstr": "-s {search_radius}",
        },
    ),
    (
        "exclusion_image_label",
        list,
        {
            "help_string": "Specify a label for the exclusion region.",
            "argstr": "-e {exclusion_image_label}",
            "requires": ["exclusion_image"],
        },
    ),
    (
        "exclusion_image",
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
        {"help_string": "Specify an exclusion region for the given label."},
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
            "help_string": "If a mask image is specified, fusion is only performed in the mask region.",
            "argstr": "-x {mask_image}",
        },
    ),
    (
        "out_label_fusion",
        Path,
        {
            "help_string": "The output label fusion image.",
            "argstr": "{out_label_fusion}",
        },
    ),
    (
        "out_intensity_fusion_name_format",
        str,
        {
            "help_string": 'Optional intensity fusion image file name format. (e.g. "antsJointFusionIntensity_%d.nii.gz")',
            "argstr": "",
        },
    ),
    (
        "out_label_post_prob_name_format",
        str,
        {
            "help_string": "Optional label posterior probability image file name format.",
            "requires": ["out_label_fusion", "out_intensity_fusion_name_format"],
        },
    ),
    (
        "out_atlas_voting_weight_name_format",
        str,
        {
            "help_string": "Optional atlas voting weight image file name format.",
            "requires": [
                "out_label_fusion",
                "out_intensity_fusion_name_format",
                "out_label_post_prob_name_format",
            ],
        },
    ),
    ("verbose", bool, {"help_string": "Verbose output.", "argstr": "-v"}),
    ("num_threads", int, 1, {"help_string": "Number of ITK threads to use"}),
]
JointFusion_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_label_fusion", Nifti1, {}),
    ("out_intensity_fusion", ty.List[File], {}),
    ("out_label_post_prob", ty.List[File], {}),
    ("out_atlas_voting_weight", ty.List[File], {}),
]
JointFusion_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class JointFusion(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.application import Dicom
    >>> from fileformats.generic import File
    >>> from fileformats.image import Bitmap, Jpeg, Tiff
    >>> from fileformats.medimage import GIPL, MetaImage, Nifti1, NiftiGz, Nrrd, NrrdGz, PGM
    >>> from pydra.tasks.ants.auto.segmentation.joint_fusion import JointFusion

    >>> task = JointFusion()
    >>> task.inputs.target_image = ["im1.nii"]
    >>> task.inputs.atlas_image = [ ["rc1s1.nii","rc1s2.nii"] ]
    >>> task.inputs.atlas_segmentation_image = ["segmentation0.nii.gz"]
    >>> task.inputs.out_label_fusion = "ants_fusion_label_output.nii"
    >>> task.cmdline
    'antsJointFusion -a 0.1 -g ["rc1s1.nii", "rc1s2.nii"] -l segmentation0.nii.gz -b 2.0 -o ants_fusion_label_output.nii -s 3x3x3 -t ["im1.nii"]'


    >>> task = JointFusion()
    >>> task.inputs.target_image = [ ["im1.nii", "im2.nii"] ]
    >>> task.cmdline
    'antsJointFusion -a 0.1 -g ["rc1s1.nii", "rc1s2.nii"] -l segmentation0.nii.gz -b 2.0 -o ants_fusion_label_output.nii -s 3x3x3 -t ["im1.nii", "im2.nii"]'


    >>> task = JointFusion()
    >>> task.inputs.atlas_image = [ ["rc1s1.nii","rc1s2.nii"],["rc2s1.nii","rc2s2.nii"] ]
    >>> task.inputs.atlas_segmentation_image = ["segmentation0.nii.gz","segmentation1.nii.gz"]
    >>> task.cmdline
    'antsJointFusion -a 0.1 -g ["rc1s1.nii", "rc1s2.nii"] -g ["rc2s1.nii", "rc2s2.nii"] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 2.0 -o ants_fusion_label_output.nii -s 3x3x3 -t ["im1.nii", "im2.nii"]'


    >>> task = JointFusion()
    >>> task.inputs.dimension = 3
    >>> task.inputs.alpha = 0.5
    >>> task.inputs.beta = 1.0
    >>> task.inputs.patch_radius = [3,2,1]
    >>> task.inputs.search_radius = [3]
    >>> task.cmdline
    'antsJointFusion -a 0.5 -g ["rc1s1.nii", "rc1s2.nii"] -g ["rc2s1.nii", "rc2s2.nii"] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 1.0 -d 3 -o ants_fusion_label_output.nii -p 3x2x1 -s 3 -t ["im1.nii", "im2.nii"]'


    >>> task = JointFusion()
    >>> task.inputs.search_radius = ["mask.nii"]
    >>> task.inputs.exclusion_image_label = ["1","2"]
    >>> task.inputs.exclusion_image = ["roi01.nii", "roi02.nii"]
    >>> task.inputs.verbose = True
    >>> task.cmdline
    'antsJointFusion -a 0.5 -g ["rc1s1.nii", "rc1s2.nii"] -g ["rc2s1.nii", "rc2s2.nii"] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 1.0 -d 3 -e 1[roi01.nii] -e 2[roi02.nii] -o ants_fusion_label_output.nii -p 3x2x1 -s mask.nii -t ["im1.nii", "im2.nii"] -v'


    >>> task = JointFusion()
    >>> task.inputs.out_label_fusion = "ants_fusion_label_output.nii"
    >>> task.inputs.out_intensity_fusion_name_format = "ants_joint_fusion_intensity_%d.nii.gz"
    >>> task.inputs.out_label_post_prob_name_format = "ants_joint_fusion_posterior_%d.nii.gz"
    >>> task.inputs.out_atlas_voting_weight_name_format = "ants_joint_fusion_voting_weight_%d.nii.gz"
    >>> task.cmdline
    'antsJointFusion -a 0.5 -g ["rc1s1.nii", "rc1s2.nii"] -g ["rc2s1.nii", "rc2s2.nii"] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 1.0 -d 3 -e 1[roi01.nii] -e 2[roi02.nii] -o [ants_fusion_label_output.nii, ants_joint_fusion_intensity_%d.nii.gz, ants_joint_fusion_posterior_%d.nii.gz, ants_joint_fusion_voting_weight_%d.nii.gz] -p 3x2x1 -s mask.nii -t ["im1.nii", "im2.nii"] -v'


    """

    input_spec = JointFusion_input_spec
    output_spec = JointFusion_output_spec
    executable = "antsJointFusion"
