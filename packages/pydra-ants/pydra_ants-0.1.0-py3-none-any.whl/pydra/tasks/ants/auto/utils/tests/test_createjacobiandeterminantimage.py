from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.create_jacobian_determinant_image import (
    CreateJacobianDeterminantImage,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_createjacobiandeterminantimage_1():
    task = CreateJacobianDeterminantImage()
    task.inputs.deformationField = NiftiGz.sample(seed=1)
    task.inputs.outputImage = NiftiGz.sample(seed=2)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_createjacobiandeterminantimage_2():
    task = CreateJacobianDeterminantImage()
    task.inputs.imageDimension = 3
    task.inputs.deformationField = NiftiGz.sample(seed=1)
    task.inputs.outputImage = NiftiGz.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
