"""
Custom test collecter, builder and runner used for examining students.
"""
import io
import unittest
import sys
from collections import OrderedDict
import test_exam
from exam_test_result import ExamTestResult

CONTACT_ERROR_MSG = (
    "\n*********\n"
    "Något gick fel i rättningsprogrammet. "
    "Kontakta Ansvarig med ovanstående felmeddelandet!"
    "\n*********"
)

PASS = 1
NOT_PASS = 0

def get_testcases(assignments):
    """
    Add all TestCases to a list and return.
    """
    testcases = []
    counter = 1
    while True:
        try:
            testcases.append(getattr(test_exam, "TestAssignment" + str(counter)))
            assignments["Assignment" + str(counter)] = {
                "pass": NOT_PASS,
            }
        except AttributeError:
            return testcases
        counter += 1



def build_testsuite(assignments):
    """
    Create TestSuit with testcases.
    """
    testcases = get_testcases(assignments)
    suite = unittest.TestSuite()
    for case in testcases:
        suite.addTest(unittest.makeSuite(case))
    return suite



def run_testcases(suite):
    """
    Run testsuit.
    """
    buf = io.StringIO()
    runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2, stream=buf)
    # runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)

    try:
        assignments_results = runner.run(suite).assignments_results
    except Exception as e:
        # Something went wrong in our code
        raise type(e)(str(e) + CONTACT_ERROR_MSG)\
            .with_traceback(sys.exc_info()[2])

    return buf.getvalue(), assignments_results



def check_pass_fail(assignments, result):
    """
    Mark assignments ass Passed if they succeded.
    """
    for assignment, outcome in result.items():
        if outcome["started"] == outcome["success"]:
            assignments[assignment]["pass"] = PASS



def format_output(output, assignments):
    """
    Print and format test run and which assignments pass/fail.
    """
    result = " ".join([str(res["pass"]) for res in assignments.values()])
    print(result)
    print(output)



def main():
    """
    Start point of program.
    """
    assignments = OrderedDict() # OrderedDict used for backwards compability
    suite = build_testsuite(assignments)
    output, assignments_results = run_testcases(suite)
    check_pass_fail(assignments, assignments_results)
    format_output(output, assignments)



if __name__ == "__main__":
    main()
