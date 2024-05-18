from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.affine_initializer import AffineInitializer
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_affineinitializer_1():
    task = AffineInitializer()
    task.inputs.dimension = 3
    task.inputs.fixed_image = Nifti1.sample(seed=1)
    task.inputs.moving_image = Nifti1.sample(seed=2)
    task.inputs.out_file = "transform.mat"
    task.inputs.search_factor = 15.0
    task.inputs.radian_fraction = 0.1
    task.inputs.principal_axes = False
    task.inputs.local_search = 10
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_affineinitializer_2():
    task = AffineInitializer()
    task.inputs.fixed_image = Nifti1.sample(seed=1)
    task.inputs.moving_image = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
