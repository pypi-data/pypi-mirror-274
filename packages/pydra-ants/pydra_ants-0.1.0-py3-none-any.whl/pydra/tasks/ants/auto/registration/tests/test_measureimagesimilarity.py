from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.registration.measure_image_similarity import (
    MeasureImageSimilarity,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_measureimagesimilarity_1():
    task = MeasureImageSimilarity()
    task.inputs.fixed_image = Nifti1.sample(seed=1)
    task.inputs.moving_image = Nifti1.sample(seed=2)
    task.inputs.metric_weight = 1.0
    task.inputs.sampling_strategy = "None"
    task.inputs.fixed_image_mask = Nifti1.sample(seed=8)
    task.inputs.moving_image_mask = NiftiGz.sample(seed=9)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_measureimagesimilarity_2():
    task = MeasureImageSimilarity()
    task.inputs.dimension = 3
    task.inputs.fixed_image = Nifti1.sample(seed=1)
    task.inputs.moving_image = Nifti1.sample(seed=2)
    task.inputs.metric = "MI"
    task.inputs.metric_weight = 1.0
    task.inputs.radius_or_number_of_bins = 5
    task.inputs.sampling_strategy = "Regular"
    task.inputs.sampling_percentage = 1.0
    task.inputs.fixed_image_mask = Nifti1.sample(seed=8)
    task.inputs.moving_image_mask = NiftiGz.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
