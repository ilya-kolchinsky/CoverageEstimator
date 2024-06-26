from transformers import AutoTokenizer, AutoModel
import torch

from CoverageEmbeddingModel import CoverageEmbeddingModel


class CodeBertEmbeddingModel(CoverageEmbeddingModel):
    def __init__(self, root_dir):
        super().__init__(root_dir)
        self.__tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.__model = AutoModel.from_pretrained("microsoft/codebert-base")

    def _embed(self, code):
        tokens = [self.__tokenizer.cls_token] + self.__tokenizer.tokenize(code) + [self.__tokenizer.eos_token]
        tokens_ids = self.__tokenizer.convert_tokens_to_ids(tokens)
        return self.__model(torch.tensor(tokens_ids)[None, :])[0]
