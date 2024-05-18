from fileformats.datascience import TextMatrix
from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.ants.auto.registration.registration import Registration
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_registration_1():
    task = Registration()
    task.inputs.dimension = 3
    task.inputs.fixed_image_mask = File.sample(seed=2)
    task.inputs.moving_image_mask = File.sample(seed=5)
    task.inputs.restore_state = TextMatrix.sample(seed=8)
    task.inputs.initial_moving_transform = [TextMatrix.sample(seed=9)]
    task.inputs.metric_weight_item_trait = 1.0
    task.inputs.radius_bins_item_trait = 5
    task.inputs.radius_or_number_of_bins = [5]
    task.inputs.use_histogram_matching = True
    task.inputs.interpolation = "Linear"
    task.inputs.write_composite_transform = False
    task.inputs.collapse_output_transforms = True
    task.inputs.initialize_transforms_per_stage = False
    task.inputs.convergence_threshold = [1e-06]
    task.inputs.convergence_window_size = [10]
    task.inputs.output_transform_prefix = "transform"
    task.inputs.winsorize_upper_quantile = 1.0
    task.inputs.winsorize_lower_quantile = 0.0
    task.inputs.verbose = False
    task.inputs.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_2():
    task = Registration()
    task.inputs.dimension = 3
    task.inputs.initial_moving_transform = [TextMatrix.sample(seed=9)]
    task.inputs.metric = ["Mattes"] * 2
    task.inputs.metric_weight = [1] * 2  # Default (value ignored currently by ANTs)
    task.inputs.radius_or_number_of_bins = [32] * 2
    task.inputs.sampling_strategy = ["Random", None]
    task.inputs.sampling_percentage = [0.05, None]
    task.inputs.use_estimate_learning_rate_once = [True, True]
    task.inputs.use_histogram_matching = [True, True]  # This is the default
    task.inputs.write_composite_transform = True
    task.inputs.collapse_output_transforms = False
    task.inputs.initialize_transforms_per_stage = False
    task.inputs.transforms = ["Affine", "SyN"]
    task.inputs.transform_parameters = [(2.0,), (0.25, 3.0, 0.0)]
    task.inputs.number_of_iterations = [[1500, 200], [100, 50, 30]]
    task.inputs.smoothing_sigmas = [[1, 0], [2, 1, 0]]
    task.inputs.sigma_units = ["vox"] * 2
    task.inputs.shrink_factors = [[2, 1], [3, 2, 1]]
    task.inputs.convergence_threshold = [1.0e-8, 1.0e-9]
    task.inputs.convergence_window_size = [20] * 2
    task.inputs.output_transform_prefix = "output_"
    task.inputs.output_warped_image = "output_warped_image.nii.gz"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_3():
    task = Registration()
    task.inputs.invert_initial_moving_transform = True
    task.inputs.winsorize_lower_quantile = 0.025
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_4():
    task = Registration()
    task.inputs.winsorize_upper_quantile = 0.975
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_5():
    task = Registration()
    task.inputs.winsorize_upper_quantile = 0.975
    task.inputs.winsorize_lower_quantile = 0.025
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_6():
    task = Registration()
    task.inputs.float = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_7():
    task = Registration()
    task.inputs.float = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_8():
    task = Registration()
    task.inputs.save_state = "trans.mat"
    task.inputs.restore_state = TextMatrix.sample(seed=8)
    task.inputs.collapse_output_transforms = True
    task.inputs.initialize_transforms_per_stage = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_9():
    task = Registration()
    task.inputs.write_composite_transform = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_10():
    task = Registration()
    task.inputs.metric = ["Mattes", ["Mattes", "CC"]]
    task.inputs.metric_weight = [1, [0.5, 0.5]]
    task.inputs.radius_or_number_of_bins = [32, [32, 4]]
    task.inputs.sampling_strategy = [
        "Random",
        None,
    ]  # use default strategy in second stage
    task.inputs.sampling_percentage = [0.05, [0.05, 0.10]]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_11():
    task = Registration()
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_12():
    task = Registration()
    task.inputs.interpolation = "BSpline"
    task.inputs.interpolation_parameters = (3,)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_13():
    task = Registration()
    task.inputs.interpolation = "Gaussian"
    task.inputs.interpolation_parameters = (1.0, 1.0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_14():
    task = Registration()
    task.inputs.transforms = ["Affine", "BSplineSyN"]
    task.inputs.transform_parameters = [(2.0,), (0.25, 26, 0, 3)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_15():
    task = Registration()
    task.inputs.fixed_image_masks = ["NULL", "fixed1.nii"]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_registration_16():
    task = Registration()
    task.inputs.initial_moving_transform = [TextMatrix.sample(seed=9)]
    task.inputs.invert_initial_moving_transform = [False, False]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
