from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.denoise_image import DenoiseImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_denoiseimage_1():
    task = DenoiseImage()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.noise_model = "Gaussian"
    task.inputs.shrink_factor = 1
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_denoiseimage_2():
    task = DenoiseImage()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_denoiseimage_3():
    task = DenoiseImage()
    task.inputs.noise_model = "Rician"
    task.inputs.shrink_factor = 2
    task.inputs.output_image = "output_corrected_image.nii.gz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_denoiseimage_4():
    task = DenoiseImage()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.save_noise = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
