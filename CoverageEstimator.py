import ast
import os.path

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

from consts import TEST_DATASET_SIZE, DEFAULT_SPLIT_TESTS, DEFAULT_SPLIT_FILES


class CoverageEstimator(object):

    def __init__(self, embedding_model, prediction_model, is_binary, binary_coverage_threshold=0):
        self.__embedding_model = embedding_model
        self.__prediction_model = prediction_model
        self.__is_binary = is_binary
        self.__binary_coverage_threshold = binary_coverage_threshold

    def load_data(self, data_path):
        return np.genfromtxt(data_path, dtype=str, delimiter=',', skip_header=1)

    def __extract_coverage_value(self, coverage_str):
        coverage = int(coverage_str)
        if self.__is_binary:
            return 0 if coverage <= self.__binary_coverage_threshold else 1
        return coverage * 0.01

    def train(self, training_set):
        can_be_trained = self.__prediction_model.can_be_trained()
        if can_be_trained:
            training_embeddings = [(self.__embedding_model.embed_path(e[0]),
                                    self.__embedding_model.embed_path(e[1]),
                                    self.__extract_coverage_value(e[2]))
                                   for e in training_set]
            self.__prediction_model.train(training_embeddings)
        return can_be_trained

    def predict(self, test_snippet, code_snippet, from_path=True,
                split_test=DEFAULT_SPLIT_TESTS, split_code=DEFAULT_SPLIT_FILES):
        if split_test:
            test_snippet_parts = self.__extract_code_parts(test_snippet, from_path, prefix="test_")
        else:
            test_snippet_parts = [test_snippet]
        test_from_path = False if split_test else from_path

        if split_code:
            code_snippet_parts = self.__extract_code_parts(code_snippet, from_path)
        else:
            code_snippet_parts = [code_snippet]
        code_from_path = False if split_code else from_path

        predictions = np.zeros((len(test_snippet_parts), len(code_snippet_parts)))
        for i, test_part in enumerate(test_snippet_parts):
            for j, code_part in enumerate(code_snippet_parts):
                predictions[i][j] = self.__predict_single(test_part, code_part, test_from_path, code_from_path)

        # For now, we return 1 if at least one of the entries of the matrix is one.
        # More complicated heuristics will follow.
        return np.any(predictions == 1.0)

    def __predict_single(self, test_snippet, code_snippet, test_from_path, code_from_path):

        test_embedding = self.__embedding_model.embed_path(test_snippet) \
            if test_from_path else self.__embedding_model.embed_code(test_snippet)
        code_embedding = self.__embedding_model.embed_path(code_snippet) \
            if code_from_path else self.__embedding_model.embed_code(code_snippet)

        return self.__prediction_model.predict_coverage(test_embedding, code_embedding)

    def __extract_code_parts(self, code_or_path, from_path, prefix=None):
        if from_path:
            full_path = self.__embedding_model.get_full_path(code_or_path)
            code = open(full_path).read()
        else:
            code = code_or_path

        tree = ast.parse(code)
        code_parts = []

        class ClassVisitor(ast.NodeVisitor):
            def visit_ClassDef(self, node):
                for item in node.body:
                    if (isinstance(item, ast.FunctionDef) and
                            not item.name.startswith("__") and
                            (prefix is None or item.name.startswith(prefix))):
                        method_code = ast.get_source_segment(code, item)
                        code_parts.append(method_code)
                self.generic_visit(node)

        class FunctionVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if prefix is None or node.name.startswith(prefix):
                    function_code = ast.get_source_segment(code, node)
                    code_parts.append(function_code)
                self.generic_visit(node)

        ClassVisitor().visit(tree)
        FunctionVisitor().visit(tree)

        if len(code_parts) == 0:
            # no methods or functions were found - presumably the code contains none
            return [code]

        return code_parts

    def evaluate(self, testing_set):
        targets = [self.__extract_coverage_value(e[2]) for e in testing_set]
        outputs = [self.predict(e[0], e[1]) for e in testing_set]

        if self.__is_binary:
            # outputs and targets are labels representing ones and zeros
            accuracy = accuracy_score(targets, outputs)
            precision = precision_score(targets, outputs, average='binary')
            recall = recall_score(targets, outputs, average='binary')
            f1 = f1_score(targets, outputs, average='binary')
            conf_matrix = confusion_matrix(targets, outputs)

            print(f'Accuracy: {accuracy:.4f}')
            print(f'Precision: {precision:.4f}')
            print(f'Recall: {recall:.4f}')
            print(f'F1 Score: {f1:.4f}')
            print('Confusion Matrix:')
            print(conf_matrix)

        else:
            # outputs and targets are percentage numbers
            mae = mean_absolute_error(targets, outputs)
            mse = mean_squared_error(targets, outputs)
            rmse = np.sqrt(mse)
            r2 = r2_score(targets, outputs)

            print(f'Mean Absolute Error (MAE): {mae:.4f}')
            print(f'Mean Squared Error (MSE): {mse:.4f}')
            print(f'Root Mean Squared Error (RMSE): {rmse:.4f}')
            print(f'R-squared (R²): {r2:.4f}')

    def apply(self, data_path):
        """
        This method basically handles data loading + train + evaluate.
        The reason we put it here is to take care of the train/test split.
        """
        dataset = self.load_data(data_path)

        ### DEBUG ###
        dataset = dataset[::100]

        if not self.__prediction_model.can_be_trained():
            self.evaluate(dataset)
            return

        training_set, testing_set = train_test_split(dataset, test_size=TEST_DATASET_SIZE)
        self.train(training_set)
        self.evaluate(testing_set)
