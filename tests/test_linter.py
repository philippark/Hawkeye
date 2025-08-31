import unittest
from src.linter import Linter

class TestLinter(unittest.TestCase):
    def setUp(self):
        self.linter = Linter("example.py")
    
    def test_line_length(self):
        source_code = "a" * 81 + "\n" + "b" * 80 + "\n"
        self.linter.run(source_code)
        self.assertIn("example.py:1 | Line exceeds 80 characters", self.linter.issues)
        self.assertNotIn("example.py:2 | Line exceeds 80 characters", self.linter.issues)
    
    def test_trailing_whitespace(self):
        source_code = "print('Hello, World!')   \nprint('No trailing space')\n"
        self.linter.run(source_code)
        self.assertIn("example.py:1 | Trailing whitespace detected", self.linter.issues)
        self.assertNotIn("example.py:2 | Trailing whitespace detected", self.linter.issues)
    
    def test_no_issues(self):
        source_code = "print('All good here')\n"
        self.linter.run(source_code)
        self.assertEqual(len(self.linter.issues), 0)

if __name__ == "__main__":
    unittest.main()