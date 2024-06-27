from CodeBertEmbeddingModel import CodeBertEmbeddingModel
from CoverageEstimator import CoverageEstimator
from SimilarityPredictionModel import SimilarityPredictionModel
from consts import *


def main():
    embedding_model = CodeBertEmbeddingModel(CODE_BASE_ROOT_DIR)
    prediction_model = SimilarityPredictionModel(BINARY_COVERAGE_MODE, SIMILARITY_THRESHOLD)
    coverage_estimator = CoverageEstimator(embedding_model, prediction_model, BINARY_COVERAGE_MODE)

    ### DEBUG ###
    #test_path = "test/units/ansible_test/test_diff.py"
    #code_path = "test/units/galaxy/test_collection.py"
    #prediction = coverage_estimator.predict(test_path, code_path)
    #print(f"Source file: {code_path}\nTest file: {test_path}\nPredicted coverage: {prediction}")

    coverage_estimator.apply(COVERAGE_DATA_PATH)


if __name__ == '__main__':
    main()
