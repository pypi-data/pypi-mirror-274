from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.threshold_image import ThresholdImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_thresholdimage_1():
    task = ThresholdImage()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.input_mask = File.sample(seed=5)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_thresholdimage_2():
    task = ThresholdImage()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.output_image = "output.nii.gz"
    task.inputs.th_low = 0.5
    task.inputs.th_high = 1.0
    task.inputs.inside_value = 1.0
    task.inputs.outside_value = 0.0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_thresholdimage_3():
    task = ThresholdImage()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.output_image = "output.nii.gz"
    task.inputs.mode = "Kmeans"
    task.inputs.num_thresholds = 4
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
