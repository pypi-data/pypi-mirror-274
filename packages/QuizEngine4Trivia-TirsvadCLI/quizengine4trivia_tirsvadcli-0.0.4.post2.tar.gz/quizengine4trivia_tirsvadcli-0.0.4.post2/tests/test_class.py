import os
import sys
import unittest

# Find the directory in which the current script resides:
src_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))
sys.path.append(src_dir)

from QuizEngine4Trivia import QuizEngine


class TestQuizEngine(unittest.TestCase):

    def test_check_return_of_next_question(self):

        app = QuizEngine()
        test_string = app.next_question()
        self.assertIsNotNone(obj=test_string)
        self.assertIs(type(test_string), str)
