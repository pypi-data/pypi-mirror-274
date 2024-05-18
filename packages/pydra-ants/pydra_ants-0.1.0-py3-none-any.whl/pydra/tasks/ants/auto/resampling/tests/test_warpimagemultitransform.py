from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.resampling.warp_image_multi_transform import (
    WarpImageMultiTransform,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warpimagemultitransform_1():
    task = WarpImageMultiTransform()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.out_postfix = "_wimt"
    task.inputs.reference_image = Nifti1.sample(seed=4)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warpimagemultitransform_2():
    task = WarpImageMultiTransform()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.reference_image = Nifti1.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warpimagemultitransform_3():
    task = WarpImageMultiTransform()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.reference_image = Nifti1.sample(seed=4)
    task.inputs.invert_affine = [
        1
    ]  # this will invert the 1st Affine file: "func2anat_coreg_Affine.txt"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
