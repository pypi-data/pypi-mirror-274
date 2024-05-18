from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.image_math import ImageMath
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_imagemath_1():
    task = ImageMath()
    task.inputs.dimension = 3
    task.inputs.op1 = Nifti1.sample(seed=3)
    task.inputs.copy_header = True
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagemath_2():
    task = ImageMath()
    task.inputs.operation = "+"
    task.inputs.op1 = Nifti1.sample(seed=3)
    task.inputs.op2 = "2"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagemath_3():
    task = ImageMath()
    task.inputs.operation = "Project"
    task.inputs.op1 = Nifti1.sample(seed=3)
    task.inputs.op2 = "1 2"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagemath_4():
    task = ImageMath()
    task.inputs.operation = "G"
    task.inputs.op1 = Nifti1.sample(seed=3)
    task.inputs.op2 = "4"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagemath_5():
    task = ImageMath()
    task.inputs.operation = "TruncateImageIntensity"
    task.inputs.op1 = Nifti1.sample(seed=3)
    task.inputs.op2 = "0.005 0.999 256"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
