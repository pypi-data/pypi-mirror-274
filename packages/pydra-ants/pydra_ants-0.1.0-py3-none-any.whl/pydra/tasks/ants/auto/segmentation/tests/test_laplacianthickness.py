from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.laplacian_thickness import LaplacianThickness
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_laplacianthickness_1():
    task = LaplacianThickness()
    task.inputs.input_wm = NiftiGz.sample(seed=0)
    task.inputs.input_gm = NiftiGz.sample(seed=1)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_laplacianthickness_2():
    task = LaplacianThickness()
    task.inputs.input_wm = NiftiGz.sample(seed=0)
    task.inputs.input_gm = NiftiGz.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_laplacianthickness_3():
    task = LaplacianThickness()
    task.inputs.output_image = "output_thickness.nii.gz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
