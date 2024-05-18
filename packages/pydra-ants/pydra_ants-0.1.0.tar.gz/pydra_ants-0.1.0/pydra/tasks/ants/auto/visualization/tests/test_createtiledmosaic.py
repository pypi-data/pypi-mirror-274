from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.visualization.create_tiled_mosaic import CreateTiledMosaic
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_createtiledmosaic_1():
    task = CreateTiledMosaic()
    task.inputs.input_image = Nifti1.sample(seed=0)
    task.inputs.rgb_image = Nifti1.sample(seed=1)
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.output_image = "output.png"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_createtiledmosaic_2():
    task = CreateTiledMosaic()
    task.inputs.input_image = Nifti1.sample(seed=0)
    task.inputs.rgb_image = Nifti1.sample(seed=1)
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.alpha_value = 0.5
    task.inputs.output_image = "output.png"
    task.inputs.direction = 2
    task.inputs.pad_or_crop = "[ -15x -50 , -15x -30 ,0]"
    task.inputs.slices = "[2 ,100 ,160]"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
