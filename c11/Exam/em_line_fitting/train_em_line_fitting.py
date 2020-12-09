"""
CSCC11 - Introduction to Machine Learning, Fall 2020, Exam
A. Shaj, B. Chan, D. Fleet
"""

import _pickle as pickle
import numpy as np

from em_line_fitting import EMLineFitting

def check_final_results(test_case, em):
    with open(f"data/test_{test_case}.pkl", "rb") as f:
        expected_results = pickle.load(f)

    assert np.allclose(expected_results["stddev"], stddevs[test_case])

    correct_ownerships = np.allclose(expected_results["ownership_probs"], em.ownership_probs)
    correct_mixing_probs = np.allclose(expected_results["mixing_probs"], em.mixing_probs)
    correct_model_params = np.allclose(expected_results["model_parameters"], em.model_parameters)

    print("=" * 75)
    print(f"Correct Ownership Probabilities: {correct_ownerships}")
    print(f"Correct Mixing Probabilities: {correct_mixing_probs}")
    print(f"Correct Model Parameters: {correct_model_params}")

    print("Details:")
    if not correct_ownerships:
        print("Expected Ownership Probabilities:")
        print(data["ownership_probs"])
        print("Got:")
        print(em.ownership_probs)

    if not correct_mixing_probs:
        print("Expected Mixing Probabilities:")
        print(data["mixing_probs"])
        print("Got:")
        print(em.mixing_probs)

    if not correct_model_params:
        print("Expected Model Parameters:")
        print(data["model_parameters"])
        print("Got:")
        print(em.model_parameters)

    print("=" * 75)
    print("\n")


if __name__ == "__main__":
    visualize = False

    # ======================================================================
    # This is for debugging purpose.
    # NOTE: Valid test_case: 0, 1, 2, 3, False
    # test_case = False -> You have control over all parameters
    # test_case = 0 -> standard deviation = 3.0, num lines = 2
    # test_case = 1 -> standard deviation = 6.0, num lines = 2
    # test_case = 2 -> standard deviation = 0.25, num lines = 2
    # test_case = 3 -> standard deviation = 0.25, num lines = 3
    # test_case = 4 -> standard deviation = 3.0, num_lines = 5
    test_case = 0
    # ======================================================================

    # ======================================================================
    # This is for your curiosity.
    # NOTE: Changing these parameters will affect the run only when you set test_case = False
    num_lines = 2
    seed = 4
    stddev = 1.0
    # ======================================================================

    assert test_case is False or test_case in list(range(5)), f"Invalid test case. Expected 0 <= test_case <= 4 or test_case = False. Got: {test_case}"
    assert num_lines > 0, f"Invalid number of lines. Expected num_lines > 0. Got: {num_lines}"

    # NOTE: We fix this seed (default: 4) so everything is deterministic
    #       Changing this will break the debugging code!
    variance = stddev ** 2
    if test_case is not False:
        seed = 4
        num_liness = np.array((2, 2, 2, 3, 5,))
        stddevs = np.array((3.0, 6.0, 0.25, 0.25, 3.0,))
        variances = stddevs ** 2
        num_lines = num_liness[test_case]
        variance = variances[test_case]

    np.random.seed(seed)
    with open("data/data.pkl", "rb") as f:
        data = pickle.load(f)

    em = EMLineFitting(data["x"],
                       data["y"],
                       num_lines,
                       np.ones(shape=(num_lines, 1), dtype=np.float) * variance,
                       visualize=visualize)

    if test_case is not False and 0 <= test_case <= 3:
        check_final_results(test_case, em)
