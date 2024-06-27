from sentence_transformers import SentenceTransformer

from CoverageEmbeddingModel import CoverageEmbeddingModel


class CodeBertEmbeddingModel(CoverageEmbeddingModel):
    def __init__(self, root_dir):
        super().__init__(root_dir)
        self.__model = SentenceTransformer('mchochlov/codebert-base-cd-ft')

    def _embed(self, code):
        return self.__model.encode(code)
