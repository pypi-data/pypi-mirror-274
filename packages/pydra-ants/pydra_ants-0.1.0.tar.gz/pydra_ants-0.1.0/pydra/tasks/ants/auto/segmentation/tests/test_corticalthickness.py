from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.cortical_thickness import CorticalThickness
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_corticalthickness_1():
    task = CorticalThickness()
    task.inputs.dimension = 3
    task.inputs.anatomical_image = Nifti1.sample(seed=1)
    task.inputs.brain_template = NiftiGz.sample(seed=2)
    task.inputs.brain_probability_mask = NiftiGz.sample(seed=3)
    task.inputs.segmentation_priors = [NiftiGz.sample(seed=4)]
    task.inputs.out_prefix = "antsCT_"
    task.inputs.image_suffix = "nii.gz"
    task.inputs.t1_registration_template = NiftiGz.sample(seed=7)
    task.inputs.extraction_registration_mask = File.sample(seed=8)
    task.inputs.cortical_label_image = Nifti1.sample(seed=17)
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_corticalthickness_2():
    task = CorticalThickness()
    task.inputs.dimension = 3
    task.inputs.anatomical_image = Nifti1.sample(seed=1)
    task.inputs.brain_template = NiftiGz.sample(seed=2)
    task.inputs.brain_probability_mask = NiftiGz.sample(seed=3)
    task.inputs.segmentation_priors = [NiftiGz.sample(seed=4)]
    task.inputs.t1_registration_template = NiftiGz.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
