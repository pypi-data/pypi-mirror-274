from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.brain_extraction import BrainExtraction
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_brainextraction_1():
    task = BrainExtraction()
    task.inputs.dimension = 3
    task.inputs.anatomical_image = Nifti1.sample(seed=1)
    task.inputs.brain_template = NiftiGz.sample(seed=2)
    task.inputs.brain_probability_mask = NiftiGz.sample(seed=3)
    task.inputs.out_prefix = "highres001_"
    task.inputs.extraction_registration_mask = File.sample(seed=5)
    task.inputs.image_suffix = "nii.gz"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_brainextraction_2():
    task = BrainExtraction()
    task.inputs.dimension = 3
    task.inputs.anatomical_image = Nifti1.sample(seed=1)
    task.inputs.brain_template = NiftiGz.sample(seed=2)
    task.inputs.brain_probability_mask = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
