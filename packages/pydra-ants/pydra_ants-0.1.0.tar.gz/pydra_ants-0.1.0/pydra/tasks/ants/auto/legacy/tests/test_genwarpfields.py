from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.legacy.gen_warp_fields import GenWarpFields
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_genwarpfields_1():
    task = GenWarpFields()
    task.inputs.dimension = 3
    task.inputs.reference_image = Nifti1.sample(seed=1)
    task.inputs.input_image = Nifti1.sample(seed=2)
    task.inputs.transformation_model = "GR"
    task.inputs.out_prefix = "ants_"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
