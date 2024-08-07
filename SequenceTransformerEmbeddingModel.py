from sentence_transformers import SentenceTransformer

from CoverageEmbeddingModel import CoverageEmbeddingModel
from consts import SEQUENCE_TRANSFORMER_TYPE


class SequenceTransformerEmbeddingModel(CoverageEmbeddingModel):
    def __init__(self, root_dir):
        super().__init__(root_dir)
        self.__model = SentenceTransformer(SEQUENCE_TRANSFORMER_TYPE)

    def _embed(self, code):
        return self.__model.encode(code)
