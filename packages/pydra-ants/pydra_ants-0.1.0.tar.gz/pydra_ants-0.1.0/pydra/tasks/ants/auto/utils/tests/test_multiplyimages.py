from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.multiply_images import MultiplyImages
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_multiplyimages_1():
    task = MultiplyImages()
    task.inputs.first_input = Nifti1.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_multiplyimages_2():
    task = MultiplyImages()
    task.inputs.dimension = 3
    task.inputs.first_input = Nifti1.sample(seed=1)
    task.inputs.second_input = 0.25
    task.inputs.output_product_image = "out.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
