from unittest import TestCase
from command.cli import main

import command.identify as id

class TestGetOperatorArtifactType(TestCase):
    def test_basic(self):
        yaml = '''
        packageName: testOperator
        channels:
        - name: alpha
        currentCSV: test-operator.v0.0.1
        '''
        if id.getOperatorArtifactType(yaml) != "packages":
            print("FAILURE")
