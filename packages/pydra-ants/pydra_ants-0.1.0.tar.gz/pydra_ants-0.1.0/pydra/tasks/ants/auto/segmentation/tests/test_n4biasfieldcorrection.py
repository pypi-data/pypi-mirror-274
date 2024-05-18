from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.n4_bias_field_correction import (
    N4BiasFieldCorrection,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_n4biasfieldcorrection_1():
    task = N4BiasFieldCorrection()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.weight_image = Nifti1.sample(seed=3)
    task.inputs.rescale_intensities = False
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_n4biasfieldcorrection_2():
    task = N4BiasFieldCorrection()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.bspline_fitting_distance = 300
    task.inputs.shrink_factor = 3
    task.inputs.n_iterations = [50, 50, 30, 20]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_n4biasfieldcorrection_3():
    task = N4BiasFieldCorrection()
    task.inputs.convergence_threshold = 1e-6
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_n4biasfieldcorrection_4():
    task = N4BiasFieldCorrection()
    task.inputs.bspline_order = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_n4biasfieldcorrection_5():
    task = N4BiasFieldCorrection()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.save_bias = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_n4biasfieldcorrection_6():
    task = N4BiasFieldCorrection()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.histogram_sharpening = (0.12, 0.02, 200)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
