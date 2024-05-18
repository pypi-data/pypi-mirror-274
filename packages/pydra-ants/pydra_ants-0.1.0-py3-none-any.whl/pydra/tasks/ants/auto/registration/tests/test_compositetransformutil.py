import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.registration.composite_transform_util import (
    CompositeTransformUtil,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_compositetransformutil_1():
    task = CompositeTransformUtil()
    task.inputs.process = "assemble"
    task.inputs.output_prefix = "transform"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_compositetransformutil_2():
    task = CompositeTransformUtil()
    task.inputs.process = "disassemble"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_compositetransformutil_3():
    task = CompositeTransformUtil()
    task.inputs.process = "assemble"
    task.inputs.out_file = "my.h5"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
