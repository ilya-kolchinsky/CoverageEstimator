# input settings
import os

COVERAGE_DATA_PATH = "/Users/ikolchin/PycharmProjects/coverage.csv"
CODE_BASE_ROOT_DIR = "/Users/ikolchin/PycharmProjects/ansible"

# model-related settings
SUPPORTED_SEQUENCE_TRANSFORMERS = (
    'mchochlov/codebert-base-cd-ft',
    'jinaai/jina-embeddings-v2-base-code',
    'WhereIsAI/UAE-Code-Large-V1',
    'davanstrien/code-prompt-similarity-model',
    'flax-sentence-embeddings/st-codesearch-distilroberta-base',
    'krlvi/sentence-t5-base-nlpl-code_search_net',
                                   )
SEQUENCE_TRANSFORMER_TYPE = SUPPORTED_SEQUENCE_TRANSFORMERS[0]
TEST_DATASET_SIZE = 0.25

# test selection settings
DEFAULT_MAX_NUMBER_OF_TESTS = 3
DEFAULT_PERCENTAGE_OF_TESTS = None
DEFAULT_MIN_METRIC_VALUE = 0.9

# binary mode settings
BINARY_COVERAGE_MODE = True
BINARY_COVERAGE_THRESHOLD = 10

# enable or disable method- or function-wise coverage prediction
DEFAULT_SPLIT_TESTS = True
DEFAULT_SPLIT_FILES = False

# similarity calculation settings
SIMILARITY_THRESHOLD = 0.4

# file collection metrics
SOURCE_FILE_EXTENSION = ".py"

# authentication
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
