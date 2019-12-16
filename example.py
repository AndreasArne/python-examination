"""
https://hackernoon.com/timing-tests-in-python-for-fun-and-profit-1663144571
"""
from unittest.runner import TextTestResult

SLOW_TEST_THRESHOLD = 0.3

class TimeLoggingTestResult(TextTestResult):

    def startTest(self, test):
        self._started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._started_at
        if elapsed > SLOW_TEST_THRESHOLD:
            name = self.getDescription(test)
            self.stream.write(
                "\n{} ({:.03}s)\n".format(
                    name, elapsed))
        super().addSuccess(test)


from unittest import TextTestRunner
class TimeLoggingTestRunner(unittest.TextTestRunner):
    
    def __init__(self, slow_test_threshold=0.3, *args, **kwargs):
        self.slow_test_threshold = slow_test_threshold
        return super().__init__(
            resultclass=TimeLoggingTestResult,
            *args,
            **kwargs,
        )

    def run(self, test):
        result = super().run(test)

        self.stream.writeln(
            "\nSlow Tests (>{:.03}s):".format(
                self.slow_test_threshold))

        for name, elapsed in result.getTestTimings():
            if elapsed > self.slow_test_threshold:
                self.stream.writeln(
                    "({:.03}s) {}".format(
                        elapsed, name))

        return result
if __name__ == '__main__':
    test_runner = TextTestRunner(resultclass=TimeLoggingTestResult)
    unittest.main(testRunner=test_runner)
