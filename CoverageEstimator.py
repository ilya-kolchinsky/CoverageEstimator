from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np


class CoverageEstimator(object):
    TEST_SIZE = 0.25

    def __init__(self, embedding_model, prediction_model, is_binary):
        self.__embedding_model = embedding_model
        self.__prediction_model = prediction_model
        self.__is_binary = is_binary

    def load_data(self, data_path):
        return np.genfromtxt(data_path, delimiter=',', skip_header=1)

    def __extract_coverage_value(self, coverage_str):
        if self.__is_binary:
            return "0" if coverage_str == "0" else "1"
        return int(coverage_str) * 0.01

    def train(self, training_set):
        can_be_trained = self.__prediction_model.can_be_trained()
        if can_be_trained:
            training_embeddings = [(self.__embedding_model.embed_path(e[0]),
                                    self.__embedding_model.embed_path(e[1]),
                                    self.__extract_coverage_value(e[2]))
                                   for e in training_set]
            self.__prediction_model.train(training_embeddings)
        return can_be_trained

    def predict(self, test_snippet, code_snippet, from_path=True):
        test_embedding = self.__embedding_model.embed_path(test_snippet) \
            if from_path else self.__embedding_model.embed_code(test_snippet)
        code_embedding = self.__embedding_model.embed_path(code_snippet) \
            if from_path else self.__embedding_model.embed_code(code_snippet)

        return self.__prediction_model.predict_coverage(test_embedding, code_embedding)

    def evaluate(self, testing_set):
        targets = [self.__extract_coverage_value(e[2]) for e in testing_set]
        outputs = [self.predict(e[0], e[1]) for e in testing_set]

        if self.__is_binary:
            # outputs and targets are labels representing ones and zeros
            accuracy = accuracy_score(targets, outputs)
            precision = precision_score(targets, outputs, average='weighted')
            recall = recall_score(targets, outputs, average='weighted')
            f1 = f1_score(targets, outputs, average='weighted')
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

        if not self.__prediction_model.can_be_trained():
            self.evaluate(dataset)
            return

        training_set, testing_set = train_test_split(dataset, test_size=self.TEST_SIZE)
        self.train(training_set)
        self.evaluate(testing_set)
