from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.average_images import AverageImages
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_averageimages_1():
    task = AverageImages()
    task.inputs.output_average_image = "average.nii"
    task.inputs.images = [Nifti1.sample(seed=3)]
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_averageimages_2():
    task = AverageImages()
    task.inputs.dimension = 3
    task.inputs.output_average_image = "average.nii.gz"
    task.inputs.normalize = True
    task.inputs.images = [Nifti1.sample(seed=3)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
