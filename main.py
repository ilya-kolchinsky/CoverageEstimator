import argparse

from CodeT5EmbeddingModel import CodeT5EmbeddingModel
from SequenceTransformerEmbeddingModel import SequenceTransformerEmbeddingModel
from CodeFileSet import GithubCodeFileSet, LocalCodeFileSet
from CoverageEstimator import CoverageEstimator
from SelectionStrategy import ConstantNumberOfTestsSelectionStrategy
from SimilarityPredictionModel import SimilarityThresholdPredictionModel
from TestPrioritizer import SimilarityBasedTestPrioritizer
from consts import *
from utils import *


def execute_test_selection(is_remote, src_file_path_or_url, test_dir_path_or_url,
                           github_token, output_tests_num, output_tests_perc):
    print("Loading test cases...")

    if is_remote:
        test_set = GithubCodeFileSet(github_url=test_dir_path_or_url, github_token=github_token)
    else:
        test_set = LocalCodeFileSet(root_dir_path=test_dir_path_or_url)

    print("Loading test prioritization model...")
    max_number_of_tests = int(output_tests_num) if output_tests_num is not None else None
    percentage_of_tests = int(output_tests_perc) if output_tests_perc is not None else None
    prioritizer = SimilarityBasedTestPrioritizer(test_set,
                                                 ConstantNumberOfTestsSelectionStrategy(max_number_of_tests,
                                                                                        percentage_of_tests),
                                                 SequenceTransformerEmbeddingModel(CODE_BASE_ROOT_DIR))

    print("Loading change set...")
    if is_remote:
        change_set = GithubCodeFileSet(file_path=src_file_path_or_url, github_token=github_token)
    else:
        change_set = LocalCodeFileSet(file_path=src_file_path_or_url)

    selected_tests = prioritizer.select(change_set)

    if len(selected_tests) == 0:
        # a rare edge case
        print("The test selection algorithm returned no tests. Please validate the input parameters.")
        return

    print("\n\nRESULTS\nThe system recommends executing the following test cases, in the following order of priority:")
    for i, t in enumerate(selected_tests):
        print(f'\t{i+1}. {t}')


def debug_test_selection(is_remote=True):
    if is_remote:
        test_set = GithubCodeFileSet(
            github_url="https://github.com/ansible/ansible/tree/devel/test/units/utils/display")
    else:
        test_set = LocalCodeFileSet(root_dir_path="/Users/ikolchin/PycharmProjects/ansible/test/units/utils/display")

    prioritizer = SimilarityBasedTestPrioritizer(test_set,
                                                 ConstantNumberOfTestsSelectionStrategy(),
                                                 SequenceTransformerEmbeddingModel(CODE_BASE_ROOT_DIR))

    if is_remote:
        change_set = GithubCodeFileSet(
            file_path="https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/sentinel.py")
    else:
        change_set = LocalCodeFileSet(file_path="/Users/ikolchin/PycharmProjects/ansible/lib/ansible/utils/sentinel.py")
    print(prioritizer.select(change_set))


def execute_coverage_evaluation():
    embedding_model = CodeT5EmbeddingModel(CODE_BASE_ROOT_DIR)
    prediction_model = SimilarityThresholdPredictionModel(BINARY_COVERAGE_MODE, SIMILARITY_THRESHOLD)
    coverage_estimator = CoverageEstimator(embedding_model, prediction_model,
                                           BINARY_COVERAGE_MODE, BINARY_COVERAGE_THRESHOLD)
    coverage_estimator.apply(COVERAGE_DATA_PATH)


def debug_coverage_evaluation():
    embedding_model = SequenceTransformerEmbeddingModel(CODE_BASE_ROOT_DIR)
    prediction_model = SimilarityThresholdPredictionModel(BINARY_COVERAGE_MODE, SIMILARITY_THRESHOLD)
    coverage_estimator = CoverageEstimator(embedding_model, prediction_model,
                                           BINARY_COVERAGE_MODE, BINARY_COVERAGE_THRESHOLD)

    test_path = "test/units/ansible_test/test_diff.py"
    code_path = "test/units/galaxy/test_collection.py"
    prediction = coverage_estimator.predict(test_path, code_path)
    print(f"Source file: {code_path}\nTest file: {test_path}\nPredicted coverage: {prediction}")


def main():
    parser = argparse.ArgumentParser(description='A tool for test selection/prioritization and coverage estimation')

    # Add arguments
    parser.add_argument('-s', '--select', help='Enable/disable test selection mode', action='store_true')
    parser.add_argument('-c', '--coverage',
                        help='Enable/disable coverage estimation mode', action='store_true')
    parser.add_argument('-r', '--remote',
                        help='Enable/disable using Github links instead of local paths', action='store_true')
    parser.add_argument('-d', '--debug', help='Enable/disable debug mode', action='store_true')

    parser.add_argument('--tests-path',
                        help='A path (local or Github link) to the folder containing the tests.')
    parser.add_argument('--change-path',
                        help='A path (local or Github link) to the file containing the changes.')
    parser.add_argument('--github-token', help='The Github token to be used.')

    parser.add_argument('--output-tests-num',
                        help='The maximal number of tests to be selected.', default=DEFAULT_MAX_NUMBER_OF_TESTS)
    parser.add_argument('--output-tests-perc',
                        help='The maximal percentage of tests to be selected.', default=DEFAULT_PERCENTAGE_OF_TESTS)

    # Parse arguments
    args = parser.parse_args()

    if args.select and args.coverage:
        parser.error("Only one of the test selection and coverage estimation modes can be selected.")
    if not args.select and not args.coverage:
        parser.error("Either the test selection mode or the coverage estimation mode must be selected.")

    if args.coverage:
        if args.debug:
            debug_coverage_evaluation()
        else:
            execute_coverage_evaluation()
    else:  # args.select == True
        if args.debug:
            debug_test_selection(args.remote)
        else:
            if not args.change_path or not args.tests_path:
                parser.error("Both the change path and the test path must be specified.")
            execute_test_selection(args.remote, args.change_path, args.tests_path,
                                   args.github_token, args.output_tests_num, args.output_tests_perc)

    # --tests-path https://github.com/ansible/ansible/tree/devel/test/units/utils/display
    # --change-path https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/sentinel.py


if __name__ == '__main__':
    main()
