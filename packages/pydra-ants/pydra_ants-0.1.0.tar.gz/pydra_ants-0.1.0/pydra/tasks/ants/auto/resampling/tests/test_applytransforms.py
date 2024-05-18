from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.resampling.apply_transforms import ApplyTransforms
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applytransforms_1():
    task = ApplyTransforms()
    task.inputs.out_postfix = "_trans"
    task.inputs.reference_image = Nifti1.sample(seed=5)
    task.inputs.interpolation = "Linear"
    task.inputs.default_value = 0.0
    task.inputs.float = False
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytransforms_2():
    task = ApplyTransforms()
    task.inputs.reference_image = Nifti1.sample(seed=5)
    task.inputs.transforms = "identity"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytransforms_3():
    task = ApplyTransforms()
    task.inputs.dimension = 3
    task.inputs.output_image = "deformed_moving1.nii"
    task.inputs.reference_image = Nifti1.sample(seed=5)
    task.inputs.interpolation = "Linear"
    task.inputs.transforms = ["ants_Warp.nii.gz", "trans.mat"]
    task.inputs.invert_transform_flags = [False, True]
    task.inputs.default_value = 0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytransforms_4():
    task = ApplyTransforms()
    task.inputs.dimension = 3
    task.inputs.output_image = "deformed_moving1.nii"
    task.inputs.reference_image = Nifti1.sample(seed=5)
    task.inputs.interpolation = "BSpline"
    task.inputs.interpolation_parameters = (5,)
    task.inputs.transforms = ["ants_Warp.nii.gz", "trans.mat"]
    task.inputs.invert_transform_flags = [False, False]
    task.inputs.default_value = 0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytransforms_5():
    task = ApplyTransforms()
    task.inputs.dimension = 3
    task.inputs.output_image = "deformed_moving1.nii"
    task.inputs.reference_image = Nifti1.sample(seed=5)
    task.inputs.interpolation = "BSpline"
    task.inputs.interpolation_parameters = (5,)
    task.inputs.transforms = ["identity", "ants_Warp.nii.gz", "trans.mat"]
    task.inputs.default_value = 0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
