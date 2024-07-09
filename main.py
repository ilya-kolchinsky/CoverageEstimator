from CodeBertEmbeddingModel import CodeBertEmbeddingModel
from CoverageEstimator import CoverageEstimator
from SimilarityPredictionModel import SimilarityThresholdPredictionModel
from consts import *
from utils import *


def main():
    embedding_model = CodeBertEmbeddingModel(CODE_BASE_ROOT_DIR)
    prediction_model = SimilarityThresholdPredictionModel(BINARY_COVERAGE_MODE, SIMILARITY_THRESHOLD)
    coverage_estimator = CoverageEstimator(embedding_model, prediction_model,
                                           BINARY_COVERAGE_MODE, BINARY_COVERAGE_THRESHOLD)

    ### DEBUG ###
    #test_path = "test/units/ansible_test/test_diff.py"
    #code_path = "test/units/galaxy/test_collection.py"
    #prediction = coverage_estimator.predict(test_path, code_path)
    #print(f"Source file: {code_path}\nTest file: {test_path}\nPredicted coverage: {prediction}")

    coverage_estimator.apply(COVERAGE_DATA_PATH)


if __name__ == '__main__':
    #main()

    #rearrange_and_group_csv(COVERAGE_DATA_PATH, COVERAGE_DATA_PATH + "_reverse.csv")
    #add_similarity_to_data(COVERAGE_DATA_PATH, COVERAGE_DATA_PATH + "_similarity.csv")

    files = list_files_in_github_directory("https://github.com/ansible/ansible/tree/devel/test/units/utils")
    print(fetch_github_file_content(files[10]))
    print('---------------------------------------------------')
    print(fetch_github_file_content("https://github.com/ansible/ansible/blob/devel/test/units/utils/test_display.py"))

