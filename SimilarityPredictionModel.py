from CoveragePredictionModel import CoveragePredictionModel

import numpy as np

from scipy.spatial.distance import *


class SimilarityThresholdPredictionModel(CoveragePredictionModel):
    def __init__(self, is_binary, similarity_threshold):
        self.__is_binary = is_binary
        self.__threshold = similarity_threshold

    @staticmethod
    def __cosine_similarity(vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    @staticmethod
    def similarity(vec1, vec2, similarity_type="cosine"):
        if similarity_type == "cosine":
            return SimilarityThresholdPredictionModel.__cosine_similarity(vec1, vec2)
        if similarity_type == "euclidean":
            return 1.0 / (1.0 + euclidean(vec1, vec2))
        if similarity_type == "manhattan":
            return 1.0 / (1.0 + cityblock(vec1, vec2))
        if similarity_type == "minkowski":
            return 1.0 / (1.0 + minkowski(vec1, vec2, 3))
        raise Exception(f"Unsupported similarity mode {similarity_type}")

    def _similarity(self, test_embedding, code_embedding):
        return self.similarity(test_embedding, code_embedding)

    def predict_coverage(self, test_embedding, code_embedding):
        similarity = self._similarity(test_embedding, code_embedding)
        if self.__is_binary:
            return 0.0 if similarity <= self.__threshold else 1.0
        # non-binary mode - a number between 0 and 1 has to be returned
        # we approximate this linearly considering everything under the threshold as zero
        return 0.0 if similarity <= self.__threshold else (similarity - self.__threshold) / (1 - self.__threshold)

    def can_be_trained(self):
        return False
