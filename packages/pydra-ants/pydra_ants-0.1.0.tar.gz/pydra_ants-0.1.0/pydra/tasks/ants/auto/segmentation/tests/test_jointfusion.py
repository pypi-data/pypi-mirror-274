from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.joint_fusion import JointFusion
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_jointfusion_1():
    task = JointFusion()
    task.inputs.alpha = 0.1
    task.inputs.beta = 2.0
    task.inputs.retain_label_posterior_images = False
    task.inputs.retain_atlas_voting_images = False
    task.inputs.constrain_nonnegative = False
    task.inputs.search_radius = [3, 3, 3]
    task.inputs.mask_image = Nifti1.sample(seed=14)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jointfusion_2():
    task = JointFusion()
    task.inputs.target_image = ["im1.nii"]
    task.inputs.atlas_image = [["rc1s1.nii", "rc1s2.nii"]]
    task.inputs.out_label_fusion = "ants_fusion_label_output.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jointfusion_3():
    task = JointFusion()
    task.inputs.target_image = [["im1.nii", "im2.nii"]]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jointfusion_4():
    task = JointFusion()
    task.inputs.atlas_image = [["rc1s1.nii", "rc1s2.nii"], ["rc2s1.nii", "rc2s2.nii"]]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jointfusion_5():
    task = JointFusion()
    task.inputs.dimension = 3
    task.inputs.alpha = 0.5
    task.inputs.beta = 1.0
    task.inputs.patch_radius = [3, 2, 1]
    task.inputs.search_radius = [3]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jointfusion_6():
    task = JointFusion()
    task.inputs.search_radius = ["mask.nii"]
    task.inputs.exclusion_image_label = ["1", "2"]
    task.inputs.verbose = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jointfusion_7():
    task = JointFusion()
    task.inputs.out_label_fusion = "ants_fusion_label_output.nii"
    task.inputs.out_intensity_fusion_name_format = (
        "ants_joint_fusion_intensity_%d.nii.gz"
    )
    task.inputs.out_label_post_prob_name_format = (
        "ants_joint_fusion_posterior_%d.nii.gz"
    )
    task.inputs.out_atlas_voting_weight_name_format = (
        "ants_joint_fusion_voting_weight_%d.nii.gz"
    )
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
