#!/usr/bin/env python3
"""
Contains testcases for the individual examination.
"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
import sys
from examiner.exam_test_case import ExamTestCase
from examiner.exam_test_result import ExamTestResult

proj_path = os.path.dirname(os.path.realpath(__file__ + "/.."))
if proj_path not in sys.path:
    sys.path.insert(0, proj_path)
#pylint: disable=wrong-import-position
import exam
#pylint: enable=wrong-import-position
#pylint: disable=attribute-defined-outside-init, line-too-long



class Test1Assignment1(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """

    def test_a_repetition(self):
        """
        Testar "repetition" funktionen.
        Förväntar sig att följande skrivs ut:
        {correct}
        Fick utskriften:
        {student}
        """
        # self.norepr = True
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exam.text_repetition()
            str_data = fake_out.getvalue().strip("\n")
            self.assertEqual(str_data, "\n".join([
                "Apa på en gata, Apa på en gata, Apa på en gata.",
                "Jag har en fin dag, Jag har en fin dag, Jag har en fin dag, Jag har en fin dag.",
                "Solen skiner idag, Solen skiner idag, Solen skiner idag.",
                "Vem är du, Vem är du, Vem är du, Vem är du, Vem är du.",
            ]))



class Test2Assignment2(ExamTestCase):
    """
    Each assignment has 2 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """
    def test_a_ceonvert(self):
        """
        Testar hextal utan 0.
        Använde följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._argument = (255, 255, 255)
        self.assertEqual(exam.convert_to_hex(self._argument), "#ffffff")
        self._argument = (230, 230, 250)
        self.assertEqual(exam.convert_to_hex(self._argument), "#e6e6fa")
        self._argument = (233, 150, 122)
        self.assertEqual(exam.convert_to_hex(self._argument), "#e9967a")
        self._argument = (34, 139, 34)
        self.assertEqual(exam.convert_to_hex(self._argument), "#228b22")

    def test_b_zeropad_hex(self):
        """
        Testar att hex tal under 10 börjar med 0.
        Använde följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._argument = (255, 48, 3)
        self.assertEqual(exam.convert_to_hex(self._argument), "#ff3003")
        self._argument = (70, 163, 10)
        self.assertEqual(exam.convert_to_hex(self._argument), "#46a30a")
        self._argument = (10, 26, 0)
        self.assertEqual(exam.convert_to_hex(self._argument), "#0a1a00")
        self._argument = (1, 2, 1)
        self.assertEqual(exam.convert_to_hex(self._argument), "#010201")



class Test3Assignment3(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """
    def test_a_no_repeating_letters(self):
        """
        Testar med ord där det inte är fler av samma bokstav.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._multi_arguments = ["abppplee", ["able", "ale", "coal", "ables"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "able")
        self._multi_arguments = ["hnopyt", ["pythons", "python", "pytho", "kangaroo"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "python")

    def test_b_with_repeating_letters(self):
        """
        Testar med ord där det finns fler av samma bokstav.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._multi_arguments = ["abppplee", ["able", "ale", "apple", "kangaroo"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "apple")
        self._multi_arguments = ["nokgrua", ["kongas", "kong", "konga", "kangaroo"]]
        self.assertEqual(exam.find_words(self._multi_arguments), "konga")
        self._multi_arguments = ["anokogrua", ["kongas", "kangarooo", "konga", "kangaroo"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "kangaroo")
        self._multi_arguments = ["hopytn", ["pytthon", "python", "pytho", "kangaroo"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "python")
        self._multi_arguments = ["hopyt", ["pytthon", "python", "pytho", "kangaroo"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "pytho")
        self._multi_arguments = ["ossb", ["boss", "sobriety", "ass"]]
        self.assertEqual(exam.find_words(*self._multi_arguments), "boss")



class Test4Assignment4(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """
    def test_a_missing_one_letter(self):
        """
        Testar med lista där bara en bokstav saknas.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._argument = ["a", "b", "d"]
        self.assertEqual(exam.missing_letters(self._argument), ["c"])
        self._argument = ["e", "f", "h", "i"]
        self.assertEqual(exam.missing_letters(self._argument), ["g"])

    def test_b_missing_multiple_letters(self):
        """
        Testar med lista där flera bokstäver saknas.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._argument = ["a", "b", "d", "e", "g"]
        self.assertEqual(exam.missing_letters(self._argument), ["c", "f"])
        self._argument = ["e", "g", "i", "k"]
        self.assertEqual(exam.missing_letters(self._argument), ["f", "h", "j"])
        self._argument = ["p", "r", "s", "t", "v"]
        self.assertEqual(exam.missing_letters(self._argument), ["q", "u"])

    def test_c_missing_multiple_trailing_letters(self):
        """
        Testar med lista där flera bokstäver efter varandra saknas.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._argument = ["c", "f"]
        self.assertEqual(exam.missing_letters(self._argument), ["d", "e"])
        self._argument = ["m", "n", "r", "s"]
        self.assertEqual(exam.missing_letters(self._argument), ["o", "p", "q"])
        self._argument = ["a", "z"]
        self.assertEqual(exam.missing_letters(self._argument), \
            ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', \
             'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y'])



class Test5Assignment5(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.

    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """
    def test_a_has_one_leapday(self):
        """
        Testar med årtal där det finns 1 skottdag.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._multi_arguments = [2016, 2017]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 1)
        self._multi_arguments = [2000, 2001]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 1)

    def test_b_has_zero_leapday(self):
        """
        Testar med årtal där det finns 0 skottdagar.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._multi_arguments = [2019, 2020]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 0)
        self._multi_arguments = [1900, 1901]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 0)
        self._multi_arguments = [2800, 2801]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 0)
        self._multi_arguments = [123456, 123456]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 0)

    def test_c_has_many_leapday(self):
        """
        Testar med årtal där det finns flera skottdagar.
        Använder följande som input
        {arguments}
        Förväntar att följande returneras:
        {correct}
        Fick följande:
        {student} 
        """
        self._multi_arguments = [2000, 2005]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 2)
        self._multi_arguments = [1234, 5678]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 1077)
        self._multi_arguments = [123456, 7891011]
        self.assertEqual(exam.leap_days(*self._multi_arguments), 1881475)



if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)
