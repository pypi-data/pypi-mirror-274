from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.visualization.convert_scalar_image_to_rgb import (
    ConvertScalarImageToRGB,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_convertscalarimagetorgb_1():
    task = ConvertScalarImageToRGB()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.output_image = "rgb.nii.gz"
    task.inputs.mask_image = "none"
    task.inputs.custom_color_map_file = "none"
    task.inputs.minimum_RGB_output = 0
    task.inputs.maximum_RGB_output = 255
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_convertscalarimagetorgb_2():
    task = ConvertScalarImageToRGB()
    task.inputs.dimension = 3
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.colormap = "jet"
    task.inputs.minimum_input = 0
    task.inputs.maximum_input = 6
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
