from consts import DEFAULT_MAX_NUMBER_OF_TESTS, DEFAULT_MIN_METRIC_VALUE


class SelectionStrategy(object):
    def select(self, prioritized_test_list):
        raise NotImplementedError()


class ConstantNumberOfTestsSelectionStrategy(SelectionStrategy):
    def __init__(self, max_number_of_tests=DEFAULT_MAX_NUMBER_OF_TESTS, min_metric_value=DEFAULT_MIN_METRIC_VALUE):
        self.__max_number_of_tests = max_number_of_tests
        self.__min_metric_value = min_metric_value

    def select(self, prioritized_test_list):
        number_of_tests_to_return = min(self.__max_number_of_tests, len(prioritized_test_list))
        while (number_of_tests_to_return > 0 and
               prioritized_test_list[number_of_tests_to_return - 1][1] < self.__min_metric_value):
            number_of_tests_to_return -= 1
        if number_of_tests_to_return == 0:
            # an edge case where no tests are similar enough to the change set - nothing to return
            return []
        return prioritized_test_list[:number_of_tests_to_return]
