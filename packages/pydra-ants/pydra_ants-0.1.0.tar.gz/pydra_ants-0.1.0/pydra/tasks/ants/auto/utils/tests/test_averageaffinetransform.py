from fileformats.datascience import TextMatrix
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.average_affine_transform import AverageAffineTransform
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_averageaffinetransform_1():
    task = AverageAffineTransform()
    task.inputs.transforms = [TextMatrix.sample(seed=2)]
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_averageaffinetransform_2():
    task = AverageAffineTransform()
    task.inputs.dimension = 3
    task.inputs.output_affine_transform = "MYtemplatewarp.mat"
    task.inputs.transforms = [TextMatrix.sample(seed=2)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
