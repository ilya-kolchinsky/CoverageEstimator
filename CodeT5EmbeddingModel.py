from transformers import AutoModel, AutoTokenizer

from CoverageEmbeddingModel import CoverageEmbeddingModel


class CodeT5EmbeddingModel(CoverageEmbeddingModel):
    def __init__(self, root_dir):
        super().__init__(root_dir)

        checkpoint = "Salesforce/codet5p-110m-embedding"

        self.__tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
        self.__model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to('mps')

    def _embed(self, code):
        inputs = self.__tokenizer.encode(code[:512], return_tensors="pt").to('mps')
        embedding = self.__model(inputs)[0]
        return embedding.detach().cpu()
