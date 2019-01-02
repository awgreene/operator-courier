from unittest import TestCase
from command.cli import main
from nose.tools import nottest
import command.identify as id

class TestGetOperatorArtifactType(TestCase):
    @nottest
    def id_test(self, file, expected ):
        yaml = open(file).read()
        actual = id.getOperatorArtifactType(yaml)
        if actual != expected:
            print("Expected " + expected + ", got " + actual)
            assert False

    def test_id_csv(self):
        self.id_test("command/tests/test_files/marketplace.v0.0.1.clusterserviceversion.yaml", "clusterServiceVersions")

    def test_id_crd(self):
        self.id_test("command/tests/test_files/marketplace-operatorsource.crd.yaml", "customResourceDefinitions")

    def test_id_package(self):
        self.id_test("command/tests/test_files/marketplace.package.yaml", "packages")

