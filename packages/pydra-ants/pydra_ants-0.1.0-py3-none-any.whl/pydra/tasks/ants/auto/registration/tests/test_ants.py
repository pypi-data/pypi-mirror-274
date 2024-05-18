import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.registration.ants import ANTS
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ants_1():
    task = ANTS()
    task.inputs.use_histogram_matching = True
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_ants_2():
    task = ANTS()
    task.inputs.dimension = 3
    task.inputs.metric = ["CC"]
    task.inputs.metric_weight = [1.0]
    task.inputs.radius = [5]
    task.inputs.output_transform_prefix = "MY"
    task.inputs.transformation_model = "SyN"
    task.inputs.gradient_step_length = 0.25
    task.inputs.use_histogram_matching = True
    task.inputs.number_of_iterations = [50, 35, 15]
    task.inputs.mi_option = [32, 16000]
    task.inputs.regularization = "Gauss"
    task.inputs.regularization_gradient_field_sigma = 3
    task.inputs.regularization_deformation_field_sigma = 0
    task.inputs.number_of_affine_iterations = [10000, 10000, 10000, 10000, 10000]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
