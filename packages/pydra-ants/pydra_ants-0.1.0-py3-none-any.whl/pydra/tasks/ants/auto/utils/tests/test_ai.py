from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.ai import AI
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ai_1():
    task = AI()
    task.inputs.dimension = 3
    task.inputs.verbose = False
    task.inputs.fixed_image = Nifti1.sample(seed=2)
    task.inputs.moving_image = Nifti1.sample(seed=3)
    task.inputs.fixed_image_mask = File.sample(seed=4)
    task.inputs.moving_image_mask = File.sample(seed=5)
    task.inputs.transform = ["Affine", 0.1]
    task.inputs.principal_axes = False
    task.inputs.search_factor = [20, 0.12]
    task.inputs.convergence = [10, 1e-06, 10]
    task.inputs.output_transform = "initialization.mat"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
