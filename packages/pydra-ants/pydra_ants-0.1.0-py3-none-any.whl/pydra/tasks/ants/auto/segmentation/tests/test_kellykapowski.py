from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.kelly_kapowski import KellyKapowski
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_kellykapowski_1():
    task = KellyKapowski()
    task.inputs.dimension = 3
    task.inputs.segmentation_image = Nifti1.sample(seed=1)
    task.inputs.gray_matter_label = 2
    task.inputs.white_matter_label = 3
    task.inputs.gray_matter_prob_image = Nifti1.sample(seed=4)
    task.inputs.white_matter_prob_image = Nifti1.sample(seed=5)
    task.inputs.convergence = "[50,0.001,10]"
    task.inputs.thickness_prior_estimate = 10
    task.inputs.thickness_prior_image = Nifti1.sample(seed=8)
    task.inputs.gradient_step = 0.025
    task.inputs.smoothing_variance = 1.0
    task.inputs.smoothing_velocity_field = 1.5
    task.inputs.number_integration_points = 10
    task.inputs.max_invert_displacement_field_iters = 20
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_kellykapowski_2():
    task = KellyKapowski()
    task.inputs.dimension = 3
    task.inputs.segmentation_image = Nifti1.sample(seed=1)
    task.inputs.convergence = "[45,0.0,10]"
    task.inputs.thickness_prior_estimate = 10
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
