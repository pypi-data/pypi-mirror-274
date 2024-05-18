from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.segmentation.atropos import Atropos
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_atropos_1():
    task = Atropos()
    task.inputs.dimension = 3
    task.inputs.intensity_images = [Nifti1.sample(seed=1)]
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.use_random_seed = True
    task.inputs.output_posteriors_name_template = "POSTERIOR_%02d.nii.gz"
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_atropos_2():
    task = Atropos()
    task.inputs.dimension = 3
    task.inputs.intensity_images = [Nifti1.sample(seed=1)]
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.initialization = "Random"
    task.inputs.number_of_tissue_classes = 2
    task.inputs.likelihood_model = "Gaussian"
    task.inputs.mrf_smoothing_factor = 0.2
    task.inputs.mrf_radius = [1, 1, 1]
    task.inputs.icm_use_synchronous_update = True
    task.inputs.maximum_number_of_icm_terations = 1
    task.inputs.n_iterations = 5
    task.inputs.convergence_threshold = 0.000001
    task.inputs.posterior_formulation = "Socrates"
    task.inputs.use_mixture_model_proportions = True
    task.inputs.save_posteriors = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_atropos_3():
    task = Atropos()
    task.inputs.dimension = 3
    task.inputs.intensity_images = [Nifti1.sample(seed=1)]
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.initialization = "KMeans"
    task.inputs.kmeans_init_centers = [100, 200]
    task.inputs.number_of_tissue_classes = 2
    task.inputs.likelihood_model = "Gaussian"
    task.inputs.mrf_smoothing_factor = 0.2
    task.inputs.mrf_radius = [1, 1, 1]
    task.inputs.icm_use_synchronous_update = True
    task.inputs.maximum_number_of_icm_terations = 1
    task.inputs.n_iterations = 5
    task.inputs.convergence_threshold = 0.000001
    task.inputs.posterior_formulation = "Socrates"
    task.inputs.use_mixture_model_proportions = True
    task.inputs.save_posteriors = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_atropos_4():
    task = Atropos()
    task.inputs.dimension = 3
    task.inputs.intensity_images = [Nifti1.sample(seed=1)]
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.initialization = "PriorProbabilityImages"
    task.inputs.prior_image = "BrainSegmentationPrior%02d.nii.gz"
    task.inputs.number_of_tissue_classes = 2
    task.inputs.prior_weighting = 0.8
    task.inputs.prior_probability_threshold = 0.0000001
    task.inputs.likelihood_model = "Gaussian"
    task.inputs.mrf_smoothing_factor = 0.2
    task.inputs.mrf_radius = [1, 1, 1]
    task.inputs.icm_use_synchronous_update = True
    task.inputs.maximum_number_of_icm_terations = 1
    task.inputs.n_iterations = 5
    task.inputs.convergence_threshold = 0.000001
    task.inputs.posterior_formulation = "Socrates"
    task.inputs.use_mixture_model_proportions = True
    task.inputs.save_posteriors = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_atropos_5():
    task = Atropos()
    task.inputs.dimension = 3
    task.inputs.intensity_images = [Nifti1.sample(seed=1)]
    task.inputs.mask_image = Nifti1.sample(seed=2)
    task.inputs.initialization = "PriorLabelImage"
    task.inputs.prior_image = "segmentation0.nii.gz"
    task.inputs.number_of_tissue_classes = 2
    task.inputs.prior_weighting = 0.8
    task.inputs.likelihood_model = "Gaussian"
    task.inputs.mrf_smoothing_factor = 0.2
    task.inputs.mrf_radius = [1, 1, 1]
    task.inputs.icm_use_synchronous_update = True
    task.inputs.maximum_number_of_icm_terations = 1
    task.inputs.n_iterations = 5
    task.inputs.convergence_threshold = 0.000001
    task.inputs.posterior_formulation = "Socrates"
    task.inputs.use_mixture_model_proportions = True
    task.inputs.save_posteriors = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
