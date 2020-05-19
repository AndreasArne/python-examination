import io
import unittest
import test_exam
from collections import OrderedDict
from exam_test_result import ExamTestResult

PASS = 1
NOT_PASS = 0

def get_testcases(assignments):
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
    testcases = get_testcases(assignments)
    suite = unittest.TestSuite()
    for case in testcases:
        suite.addTest(unittest.makeSuite(case))
    return suite



def run_tests(suite):
    buf = io.StringIO()
    runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2, stream=buf)
    assignments_results = runner.run(suite).assignments_results
    return buf.getvalue(), assignments_results



def check_pass_fail(assignments, result):
    for assignment, outcome in result.items():
        if outcome["started"] == outcome["success"]:
            assignments[assignment]["pass"] = PASS



def format_output(output, assignments):
    result = "".join([str(res["pass"]) for res in assignments.values()])
    print(result)
    print(output)



if __name__ == "__main__":
    assignments = OrderedDict() # OrderedDict used for backwards compability
    suite = build_testsuite(assignments)
    output, assignments_results = run_tests(suite)
    check_pass_fail(assignments, assignments_results)
    final_output = format_output(output, assignments)
    # print(final_output)
