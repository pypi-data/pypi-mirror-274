from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.resampling.warp_time_series_image_multi_transform import (
    WarpTimeSeriesImageMultiTransform,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warptimeseriesimagemultitransform_1():
    task = WarpTimeSeriesImageMultiTransform()
    task.inputs.dimension = 4
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.out_postfix = "_wtsimt"
    task.inputs.reference_image = Nifti1.sample(seed=3)
    task.inputs.transformation_series = [NiftiGz.sample(seed=8)]
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warptimeseriesimagemultitransform_2():
    task = WarpTimeSeriesImageMultiTransform()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.reference_image = Nifti1.sample(seed=3)
    task.inputs.transformation_series = [NiftiGz.sample(seed=8)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warptimeseriesimagemultitransform_3():
    task = WarpTimeSeriesImageMultiTransform()
    task.inputs.input_image = Nifti1.sample(seed=1)
    task.inputs.reference_image = Nifti1.sample(seed=3)
    task.inputs.transformation_series = [NiftiGz.sample(seed=8)]
    task.inputs.invert_affine = [
        1
    ]  # # this will invert the 1st Affine file: ants_Affine.txt
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
