from fileformats.datascience import TextMatrix
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.compose_multi_transform import ComposeMultiTransform
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_composemultitransform_1():
    task = ComposeMultiTransform()
    task.inputs.dimension = 3
    task.inputs.reference_image = Nifti1.sample(seed=2)
    task.inputs.transforms = [TextMatrix.sample(seed=3)]
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_composemultitransform_2():
    task = ComposeMultiTransform()
    task.inputs.dimension = 3
    task.inputs.transforms = [TextMatrix.sample(seed=3)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
