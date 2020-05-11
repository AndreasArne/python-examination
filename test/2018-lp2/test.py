#!/usr/bin/env python3

from unittest import TextTestRunner
from unittest.mock import patch
from importlib import util
from io import StringIO
import unittest
from unittest import TestCase

import os
import sys

proj_path = os.path.dirname(os.path.realpath(__file__ + "/../../../app"))
if proj_path not in sys.path:
    sys.path.insert(0, proj_path)
#pylint: disable=wrong-import-position
import exam
from app.exam_test_result import ExamTestResult
#pylint: enable=wrong-import-position

"""
https://stackoverflow.com/questions/26044977/python-3-unittest-how-to-extract-results-of-tests
https://github.com/python/cpython/tree/master/Lib/unittest
"""

unittest.util._MAX_LENGTH=2000

class TestFunc(unittest.TestCase):

    def test_a_module(self):
        """
        Testar
        Förväntat resultat: {correct}
        Fick som resultat:  {student}
        """
        # self.assertEqual(0, 1)
        hej = 4
        "hej" - 4

    #
    # def test_b_module(self):
    #     """
    #     hej pa er
    #     Producerar fel för testprogrammet, ger CONTACT_ERROR_MSG
    #     """
    #     # try:
    #     # hej = 4
    #     # "hej" - 4
    #     self.assertIsNotNone(None)

    # def test_c_module(self):
    #     # try:
    #     self.assertTrue(0)
        # except Exception as e:
            # pass
            # print(e.__class__)
            # print(e.args)
            # print(e.__dict__)

            # raise

class TestAssignment1(TestCase):
    """
    Assignment 1
    """

    def test_a_text_repetition(self):
        """
        Din funktion skriver inte ut texten i rätt format.
        Förväntat resultat: {correct}
        Fick som resultat:  {student}
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exam.text_repetition()
            str_data = fake_out.getvalue().strip("\n")
            list_data = str_data.split("\n")
            self.assertEqual(list_data, [
                "Apa på en gata, Apa på en gata, Apa på en gata.",
                "Jag har en fin dag, Jag har en fin dag, Jag har en fin dag, Jag har en fin dag.",
                "Solen skiner idag, Solen skiner idag, Solen skiner idag.",
                "Vem är du, Vem är du, Vem är du, Vem är du, Vem är du.",
            ])
    def test_c_text_repetition(self):
        """
        Din funktion skriver inte ut texten i rätt format.
        Förväntat resultat: {correct}
        Fick som resultat:  {student}
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exam.text_repetition()
            str_data = fake_out.getvalue().strip("\n")
            list_data = str_data.split("\n")
            self.assertEqual(list_data, [
                "Ap på en gata, Apa på en gata, Apa på en gata.",
                "Jag har en fin dag, Jag har en fin dag, Jag har en fin dag, Jag har en fin dag.",
                "Solen skiner idag, Solen skiner idag, Solen skiner idag.",
                "V  em är du, Vem är du, Vem är du, Vem är du, Vem är du.",
            ])

class TestAssignment2(TestCase):
    """
    Assignment 2
    """
    def test_convert_to_hex(self):
        """
        Du kan inte konvertera färger
        Argument till funktionen: {arguments}
        Förväntat resultat: {correct}
        Fick som resultat:  {student}
        """
        self.assertEqual(exam.convert_to_hex((255, 255, 255)), "#fffff1")
        self.assertEqual(exam.convert_to_hex((255, 0, 0)), "#ff0000")
        self.assertEqual(exam.convert_to_hex((0, 255, 255)), "#00ffff")
        self.assertEqual(exam.convert_to_hex((230, 230, 250)), "#e6e6fa")
        self.assertEqual(exam.convert_to_hex((233, 150, 122)), "#e9967a")
        self.assertEqual(exam.convert_to_hex((34, 139, 34)), "#228b22")
        self.assertEqual(exam.convert_to_hex((255, 170, 00)), "#ffaa00")

    def test_b_convert_to_hex(self):
        """
        Du kan inte konvertera färger
        Argument till funktionen: {arguments}
        Förväntat resultat: {correct}
        Fick som resultat:  {student}
        """
        self.assertEqual(exam.convert_to_hex((255, 255, 255)), "#ffffff")
        self.assertEqual(exam.convert_to_hex((255, 0, 0)), "#ff0001")
        self.assertEqual(exam.convert_to_hex((0, 255, 255)), "#00ffff")
        self.assertEqual(exam.convert_to_hex((230, 230, 250)), "#e6e6fa")
        self.assertEqual(exam.convert_to_hex((233, 150, 122)), "#e9967a")
        self.assertEqual(exam.convert_to_hex((34, 139, 34)), "#228b22")
        self.assertEqual(exam.convert_to_hex((255, 170, 00)), "#ffaa00")
    #
    # def test_d_calculate_score(self):
    #     """
    #     Test assignment 3
    #     """
    #     self.assertEqual(exam.calculate_score("a"), "a:1")
    #     self.assertEqual(exam.calculate_score("dbbaCEDbdAacbCEAadcB"), "b:3, d:2, a:1, c:0, e:-2")
    #     self.assertEqual(exam.calculate_score("EbAAdbBEaBaaBBdAcecebeeebaec"), "e:4, c:3, d:2, a:1, b:0")
    #
    # def test_e_find_missing(self):
    #     """
    #     Test assignment 4
    #     """
    #     self.assertEqual(exam.find_missing([2, 4, 6, 3, 8, 7]), [5,])
    #     self.assertEqual(exam.find_missing([42, 46, 47, 48, 43]), [44, 45])
    #     self.assertEqual(exam.find_missing([2, 4, 3, 8, 7]), [5, 6])
    #     self.assertEqual(exam.find_missing([2, 4, 8, 7]), [3, 5, 6])
    #     self.assertEqual(exam.find_missing([-1, 2, 4, 3, 8, 7]), [0, 1, 5, 6])
    #
    #
    # def test_f_add_range(self):
    #     """
    #     Test assignment 5
    #     """
    #     inp = ["15", "-15", "0", "100", "-50", "l", "q"]
    #     with patch('builtins.input', side_effect=inp):
    #         with patch('sys.stdout', new=StringIO()) as fake_out:
    #             exam.add_range()
    #             str_data = fake_out.getvalue().strip("\n")
    #             list_data = str_data.split("\n")
    #             self.assertEqual(list_data, ["45", "-45", "0", "2103", "-503", "Input an integer"])



if __name__ == '__main__':
    runner = TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner)#, testLoader=ExamTestLoader())
    # unittest.main(testRunner=runner, testLoader=ExamTestLoader())
