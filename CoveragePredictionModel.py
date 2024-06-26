class CoveragePredictionModel(object):
    """
    The base class for coverage prediction models.
    """
    def predict_coverage(self, test_embedding, code_embedding):
        raise NotImplementedError()

    def can_be_trained(self):
        raise NotImplementedError()

    def train(self, training_set):
        raise NotImplementedError()
