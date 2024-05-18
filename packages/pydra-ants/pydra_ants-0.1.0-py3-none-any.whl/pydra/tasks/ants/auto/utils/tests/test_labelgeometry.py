from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.utils.label_geometry import LabelGeometry
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_labelgeometry_1():
    task = LabelGeometry()
    task.inputs.dimension = 3
    task.inputs.label_image = Nifti1.sample(seed=1)
    task.inputs.intensity_image = Nifti1.sample(seed=2)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_labelgeometry_2():
    task = LabelGeometry()
    task.inputs.dimension = 3
    task.inputs.label_image = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_labelgeometry_3():
    task = LabelGeometry()
    task.inputs.intensity_image = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
