from CodeBertEmbeddingModel import CodeBertEmbeddingModel
from CodeFileSet import GithubCodeFileSet, LocalCodeFileSet
from CoverageEstimator import CoverageEstimator
from SelectionStrategy import ConstantNumberOfTestsSelectionStrategy
from SimilarityPredictionModel import SimilarityThresholdPredictionModel
from TestPrioritizer import SimilarityBasedTestPrioritizer
from consts import *
from utils import *


def main():
    test_set = LocalCodeFileSet(root_dir_path="/Users/ikolchin/PycharmProjects/ansible/test/units/utils/display")

    prioritizer = SimilarityBasedTestPrioritizer(test_set,
                                                 ConstantNumberOfTestsSelectionStrategy(),
                                                 CodeBertEmbeddingModel(CODE_BASE_ROOT_DIR))

    change_set = LocalCodeFileSet(file_path="/Users/ikolchin/PycharmProjects/ansible/lib/ansible/utils/sentinel.py")
    print(prioritizer.select(change_set))

    #embedding_model = CodeBertEmbeddingModel(CODE_BASE_ROOT_DIR)
    #prediction_model = SimilarityThresholdPredictionModel(BINARY_COVERAGE_MODE, SIMILARITY_THRESHOLD)
    #coverage_estimator = CoverageEstimator(embedding_model, prediction_model,
    #                                       BINARY_COVERAGE_MODE, BINARY_COVERAGE_THRESHOLD)

    ### DEBUG ###
    #test_path = "test/units/ansible_test/test_diff.py"
    #code_path = "test/units/galaxy/test_collection.py"
    #prediction = coverage_estimator.predict(test_path, code_path)
    #print(f"Source file: {code_path}\nTest file: {test_path}\nPredicted coverage: {prediction}")

    #coverage_estimator.apply(COVERAGE_DATA_PATH)


if __name__ == '__main__':
    main()

    #rearrange_and_group_csv(COVERAGE_DATA_PATH, COVERAGE_DATA_PATH + "_reverse.csv")
    #add_similarity_to_data(COVERAGE_DATA_PATH, COVERAGE_DATA_PATH + "_similarity.csv")

    #files = LocalCodeFileSet("/Users/ikolchin/PycharmProjects/ansible/test/units/utils")
    #files = GithubCodeFileSet("https://github.com/ansible/ansible/tree/devel/test/units/utils")
    #print(files.path_to_code(files.get_file_paths()[10]))
    #print('---------------------------------------------------')
    #print(files.path_to_code("https://github.com/ansible/ansible/blob/devel/test/units/utils/test_display.py"))

