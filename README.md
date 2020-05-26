This repository contain code for examining students on College level in an introduction python course.

`app/exam_test_result.py` - overshadows methods in [unittest.TextTestResult](https://github.com/python/cpython/blob/master/Lib/unittest/runner.py#L29) to customize the output from unittest.

`test/test_copy_of_unittest.py` - Is a copy of the test file for the sourcecode of unittest. Is used to limit how much we break the original usage of unitest.

`test/test_exam_text_result.py` - Contains tests for the new functionality of the TextTestResult class.

`test/2018-lp2/test.py` - Contains a running example of the exam_test_result.py code.

# TODO:
- [ ] How to handle "empty" exam.py?
- [ ] Test it for multiple python versions (Tox?)
- [ ] Try `_mult_arguments`.
- [ ] Package so students also get colorama module
- [ ] Write tests
    - Add test in test_exam_text_result for the added functionality.
- [ ] Try removing escaped newlines from output so CONTACT_ERROR_MSG is displayed correctly for all errors.
    - Identify errors where this happens.
- [ ] Add help text for common errors, such as too many inputs when mocking.
- [ ] Don't show same error, from different tests for same error.
