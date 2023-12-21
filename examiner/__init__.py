"""
Meta data for code
"""
from examiner.exam_test_case import ExamTestCase
from examiner.exam_test_case_exam import ExamTestCaseExam
from examiner.exam_test_result import ExamTestResult
from examiner.exam_test_result_exam import ExamTestResultExam
from examiner.helper_functions import check_for_tags as tags, find_path_to_assignment, import_module

# Version structure major.minor[.patch][sub]
__version__ = '2.4.0'


# Hur gör vi för att release ska vara kursspecifik?
# Stoppa in via Github Actions när koden pushas till repon?
# Lägga det i en fil i kursrepot?
# Samma sak med dsn url:en, vill vi hårdkoda den här?
# Lägg det i en funktion som vi anropar från test filerna, då blir det mer opt in än default igång?
# 

import sentry_sdk
# config https://docs.sentry.io/platforms/python/configuration/options/
sentry_sdk.init(
    dsn="url",
    send_default_pii=False,
    send_client_reports=False,
    server_name="Jane Doe",
    release="oopython@vt24",
    sample_rate=1.0, # ändra denna för att inte bli för spammad?
)

# Använd tags för att specificera kmom i suite filerna? 
# https://docs.sentry.io/platforms/python/enriching-events/tags/

# läs om https://docs.sentry.io/platforms/python/enriching-events/scopes/