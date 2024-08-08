import os.path


class CoverageEmbeddingModel(object):
    """
    The base class for various embeddings applied on the source/test files.
    """
    def __init__(self, root_dir):
        self.__root = root_dir

    def embed_path(self, file_path):
        full_path = self.get_full_path(file_path)
        code = open(full_path).read()
        return self.embed_code(code)

    def get_full_path(self, file_path):
        return os.path.join(self.__root, file_path)

    def embed_code(self, code_snippet):
        return self._embed(code_snippet)

    def _embed(self, code):
        raise NotImplementedError()

