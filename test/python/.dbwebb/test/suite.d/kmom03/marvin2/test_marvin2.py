#!/usr/bin/env python3
"""
An autogenerated testfile for python.
"""

import unittest
from unittest.mock import patch
from io import StringIO
import re
import os
import sys
import inspect
from unittest import TextTestRunner
from examiner import tags, ExamTestCase, ExamTestResult
from examiner import import_module, find_path_to_assignment


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = find_path_to_assignment(FILE_DIR)

if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

# Path to file and basename of the file to import
main = import_module(REPO_PATH, 'main')
marvin = import_module(REPO_PATH, 'marvin')


class Test2Marvin2NewMenus(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.
    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """

    @classmethod
    def setUpClass(cls):
        """
        To find all relative files that are read or written to.
        """
        os.chdir(REPO_PATH)


    def check_print_contain(self, inp, correct, func):
        """
        One function for testing print input functions.
        """
        with patch("builtins.input", side_effect=inp):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                func()
                str_data = fake_out.getvalue()
                for val in correct:
                    self.assertIn(val, str_data)


    @tags("8", "marvin2")
    def test_randomize_string_menu(self):
        """
        Testar att anropa menyval 8 via main funktionen i main.py.
        Använder följande som input:
        {arguments}
        Förväntar att följande sträng finns med i utskrift fast med bokstäverna i annan ordning:
        {correct}
        Fick följande:
        {student}
        """
        string = "Borde inte bli samma igen"
        self._multi_arguments = ["8", string, "", "q"]

        with patch("builtins.input", side_effect=self._multi_arguments):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main.main()
                str_data = fake_out.getvalue()

        length = len(string)
        pattern = fr"{string} --> ([{string}]{{{length}}})"

        self.student_answer = repr(str_data)
        self.correct_answer = repr(string)


        try:
            rnd_str = re.search(pattern, str_data)[1]
        except TypeError:
            raise AssertionError
        if string == rnd_str or sorted(string) != sorted(rnd_str):
            raise AssertionError



    @tags("8", "marvin2")
    def test_randomize_string_func(self):
        """
        Testar att anropa funktionen randomize_string i marvin.py.
        Använder följande som argument:
        {arguments}
        Förväntar att följande sträng returneras, fast med bokstäverna i annan ordning:
        {correct}
        Fick följande:
        {student}
        """
        string = "MedSiffror1234567890"
        self._argument = string

        str_data = marvin.randomize_string(string)

        length = len(string)
        pattern = fr"{string} --> ([{string}]{{{length}}})"

        self.student_answer = str_data
        self.correct_answer = repr(string)

        try:
            rnd_str = re.search(pattern, str_data)[1]
        except TypeError:
            raise AssertionError
        if string == rnd_str or sorted(string) != sorted(rnd_str):
            raise AssertionError



    @tags("9", "marvin2")
    def test_get_acronym_menu(self):
        """
        Testar att anropa menyval 9 via main funktionen i main.py.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = ["9", "BRöderna Ivarsson Osby", "", "q"]
        self.check_print_contain(
            self._multi_arguments,
            ["BRIO"],
            main.main
        )



    @tags("9", "marvin2")
    def test_get_acronym_func(self):
        """
        Testar att anropa funktionen get_acronym i marvin.py.
        Använder följande som argument:
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student}
        """
        self._argument = "Ingvar Kamprad Elmtaryd Agunnaryd"
        self.assertEqual(
            marvin.get_acronym(self._argument),
            "IKEA"
        )



    @tags("10", "marvin2")
    def test_mask_string_menu(self):
        """
        Testar att anropa menyval 10 via main funktionen i main.py.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = ["10", "4556364607935616", "", "q"]
        self.check_print_contain(
            self._multi_arguments,
            ["############5616"],
            main.main
        )



    @tags("10", "marvin2")
    def test_mask_string_func(self):
        """
        Testar att anropa funktionen mask_string i marvin.py.
        Använder följande som argument:
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student}
        """
        self._argument = "Hej Hej"
        self.assertEqual(
            marvin.mask_string(self._argument),
            "### Hej"
        )



    @tags("10", "marvin2")
    def test_mask_string_check_use_multiply_func(self):
        """
        Testar att funktionen mask_string anropar funktionen multiply_str.
        Förväntar att anrop görs i koden:
        {correct}
        Din funktion innehåller följande:
        {student}
        """
        self.norepr = True
        self.assertIn(
            "multiply_str(",
            inspect.getsource(marvin.mask_string)
        )



    @tags("10", "3", "marvin2")
    def test_multiply_str_func(self):
        """
        Testar att anropa funktionen multiply_str i marvin.py.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self._multi_arguments = ["#", 5]
        res = marvin.multiply_str(*self._multi_arguments)
        self.assertEqual("#####", res)



    @tags("11", "marvin2")
    def test_find_all_indexes_menu(self):
        """
        Testar att anropa menyval 11 i main.py.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskriften:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = [
            "11",
            "There's unlimited juice? This party is gonna be off the hook. Oh, I'm sorry, I forgot... your wife is dead!.",
            "is",
            "",
            "q"
        ]

        self.check_print_contain(
            self._multi_arguments,
            ["27,36,99"],
            main.main
        )



    @tags("11", "marvin2")
    def test_find_all_indexes_includes_last(self):
        """
        Testar att anropa funktionen find_all_indexes i marvin.py. Där sista karaktären också ska hittas.
        Använder följande som input:
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student}
        """
        self._multi_arguments = [
            "There's unlimited juice? This party is gonna be off the hook. Oh, I'm sorry, I forgot... your wife is dead!.",
            "."
        ]

        self.assertEqual(
                marvin.find_all_indexes(
                *self._multi_arguments
            ),
            "60,85,86,87,107"
        )



    @tags("11", "marvin2")
    def test_find_all_indexes_missing(self):
        """
        Testar att anropa funktionen find_all_indexes i marvin.py. Där söksträngen saknas.
        Använder följande som input:
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student}
        """
        self._multi_arguments = [
            "There's unlimited juice? This party is gonna be off the hook. Oh, I'm sorry, I forgot... your wife is dead!.",
            "x"
        ]

        self.assertEqual(
                marvin.find_all_indexes(
                *self._multi_arguments
            ),
            ""
        )



    @tags("11", "marvin2")
    def test_find_all_indexes_check_use_try_except(self):
        """
        Testar att funktionen find_all_indexes innehåller try och except konstruktionen.
        Förväntar att följande rad finns i din funktion:
        {correct}
        Din funktion innehåller följande:
        {student}
        """
        self.norepr = True
        self.assertIn("try:", inspect.getsource(marvin.find_all_indexes))
        self.assertIn("except ValueError:", inspect.getsource(marvin.find_all_indexes))



if __name__ == '__main__':
    runner = TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)