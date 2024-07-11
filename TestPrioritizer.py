from SimilarityPredictionModel import SimilarityThresholdPredictionModel


class TestPrioritizer(object):

    def __init__(self, test_set, selection_strategy):
        self._test_set = test_set
        self.__selection_strategy = selection_strategy
        self._current_priority_list = None
        self._current_priority_dict = None

    def prioritize(self, change_set):
        # We assume self._prioritize returns a list of tuples where each tuple contains 3 fields:
        # - a path from the test set
        # - a metric according to which the paths were sorted
        # - arbitrary metadata for use by subclasses
        # We only return the paths to the user and keep the metrics internally
        self._current_priority_list = self._prioritize(change_set)
        self._current_priority_dict = {path: metric for path, metric, _ in self._current_priority_list}
        return [p for p, _, _ in self._current_priority_list]

    def select(self, change_set):
        self.prioritize(change_set)
        # apply a selection strategy from a subclass
        filtered_list = self.__selection_strategy.select(self._current_priority_list)
        return [p for p, _, _ in filtered_list]

    def _prioritize(self, change_set):
        raise NotImplementedError()


class SimilarityBasedTestPrioritizer(TestPrioritizer):
    # TODO: this atrocious code urgently requires refactoring jointly with CoverageEstimator
    def __init__(self, test_set, selection_strategy, embedding_model):
        super().__init__(test_set, selection_strategy)
        self.__embedding_model = embedding_model

    def _prioritize(self, change_set):
        change_paths_num = len(change_set.get_file_paths())
        if change_paths_num > 1:
            raise NotImplementedError("Change sets of multiple files are not supported in this version.")

        changed_file_path = change_set.get_file_paths()[0]
        print(f'Processing modified source file {changed_file_path}...')
        changed_file_code = change_set.path_to_code(changed_file_path)
        code_embedding = self.__embedding_model.embed_code(changed_file_code)

        result = []

        for test_path, test_code in self._test_set.get_content():
            print(f'Processing test file {test_path}...')
            test_embedding = self.__embedding_model.embed_code(test_code)
            similarity = SimilarityThresholdPredictionModel.similarity(code_embedding, test_embedding)
            result.append((test_path, similarity, None))

        print("Selecting test cases to recommend...")
        return sorted(result, key=lambda x: x[1], reverse=True)
