from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.resample_image_by_spacing import ResampleImageBySpacing
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_resampleimagebyspacing_1():
    task = ResampleImageBySpacing()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_resampleimagebyspacing_2():
    task = ResampleImageBySpacing()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.output_image = "output.nii.gz"
    task.inputs.out_spacing = (4, 4, 4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_resampleimagebyspacing_3():
    task = ResampleImageBySpacing()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.output_image = "output.nii.gz"
    task.inputs.out_spacing = (4, 4, 4)
    task.inputs.apply_smoothing = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_resampleimagebyspacing_4():
    task = ResampleImageBySpacing()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.output_image = "output.nii.gz"
    task.inputs.out_spacing = (0.4, 0.4, 0.4)
    task.inputs.apply_smoothing = True
    task.inputs.addvox = 2
    task.inputs.nn_interp = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
