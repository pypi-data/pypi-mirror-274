from fileformats.datascience import TextMatrix
from fileformats.text import Csv
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.resampling.apply_transforms_to_points import (
    ApplyTransformsToPoints,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applytransformstopoints_1():
    task = ApplyTransformsToPoints()
    task.inputs.input_file = Csv.sample(seed=1)
    task.inputs.transforms = [TextMatrix.sample(seed=3)]
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytransformstopoints_2():
    task = ApplyTransformsToPoints()
    task.inputs.dimension = 3
    task.inputs.input_file = Csv.sample(seed=1)
    task.inputs.transforms = [TextMatrix.sample(seed=3)]
    task.inputs.invert_transform_flags = [False, False]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
