from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.legacy.buildtemplateparallel import buildtemplateparallel
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_buildtemplateparallel_1():
    task = buildtemplateparallel()
    task.inputs.dimension = 3
    task.inputs.out_prefix = "antsTMPL_"
    task.inputs.in_files = [Nifti1.sample(seed=2)]
    task.inputs.parallelization = 0
    task.inputs.iteration_limit = 4
    task.inputs.transformation_model = "GR"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_buildtemplateparallel_2():
    task = buildtemplateparallel()
    task.inputs.in_files = [Nifti1.sample(seed=2)]
    task.inputs.max_iterations = [30, 90, 20]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
