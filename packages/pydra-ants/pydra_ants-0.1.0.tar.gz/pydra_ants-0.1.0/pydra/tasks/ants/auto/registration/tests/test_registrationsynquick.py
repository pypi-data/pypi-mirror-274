import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.registration.registration_syn_quick import (
    RegistrationSynQuick,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_registrationsynquick_1():
    task = RegistrationSynQuick()
    task.inputs.dimension = 3
    task.inputs.output_prefix = "transform"
    task.inputs.num_threads = 1
    task.inputs.transform_type = "s"
    task.inputs.histogram_bins = 32
    task.inputs.spline_distance = 26
    task.inputs.precision_type = "double"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registrationsynquick_2():
    task = RegistrationSynQuick()
    task.inputs.num_threads = 2
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registrationsynquick_3():
    task = RegistrationSynQuick()
    task.inputs.num_threads = 2
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
