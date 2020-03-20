import sys
import unittest
from unittest.runner import _WritelnDecorator
from app.exam_test_result import ExamTestResult



class Test_TestResult(unittest.TestCase):

    def test_startTest(self):
        """
        Tests the overshadowed method `startTest`.
        """
        class TestAssignment1(unittest.TestCase):
            def test_a_foo(self):
                pass
            def test_b_bar(self):
                pass

        test = TestAssignment1('test_a_foo')
        test2 = TestAssignment1('test_b_bar')

        result = ExamTestResult(_WritelnDecorator(sys.stderr), True, 2)

        result.startTest(test)
        result.startTest(test2)
        
        self.assertEqual(result.ASSIGNEMTS_STARTED, ['_TestResult.test_startTest.<locals>.TestAssignment1'])
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 2)
        self.assertEqual(result.shouldStop, False)

        result.stopTest(test)

if __name__ == '__main__':
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(verbosity=2)