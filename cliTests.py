from unittest import TestCase
from command.cli import main

class TestCli(TestCase):
    def test_basic(self):
        main()
