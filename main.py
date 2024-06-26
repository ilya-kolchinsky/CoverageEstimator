from CodeBertEmbeddingModel import CodeBertEmbeddingModel
from CoverageEstimator import CoverageEstimator
from SimilarityPredictionModel import SimilarityPredictionModel

# input settings
COVERAGE_DATA_PATH = ""
CODE_BASE_ROOT_DIR = ""

# advanced settings
BINARY_COVERAGE_MODE = True
SIMILARITY_THRESHOLD = 0.6


def main():
    embedding_model = CodeBertEmbeddingModel(CODE_BASE_ROOT_DIR)
    prediction_model = SimilarityPredictionModel(BINARY_COVERAGE_MODE, SIMILARITY_THRESHOLD)

    coverage_estimator = CoverageEstimator(embedding_model, prediction_model, BINARY_COVERAGE_MODE)
    coverage_estimator.apply(COVERAGE_DATA_PATH)


if __name__ == '__main__':
    main()
