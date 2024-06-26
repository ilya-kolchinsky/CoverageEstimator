from sklearn.metrics.pairwise import cosine_similarity
from CoveragePredictionModel import CoveragePredictionModel


class SimilarityPredictionModel(CoveragePredictionModel):
    def __init__(self, is_binary, similarity_threshold):
        self.__is_binary = is_binary
        self.__threshold = similarity_threshold

    def predict_coverage(self, test_embedding, code_embedding):
        similarity = cosine_similarity(test_embedding, code_embedding)
        if self.__is_binary:
            return "0" if similarity < self.__threshold else "1"
        # non-binary mode - a number between 0 and 1 has to be returned
        # we approximate this linearly considering everything under the threshold as zero
        return 0.0 if similarity < self.__threshold else (similarity - self.__threshold) / (1 - self.__threshold)

    def can_be_trained(self):
        return False
