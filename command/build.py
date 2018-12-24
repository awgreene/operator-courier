import yaml

class BuildCmd():
    name = 'build'
    operatorArtifactsTemplate = dict(
        data = dict( 
            customResourceDefinitions = [],
            clusterServiceVersions = [],
            packages = [], 
        )
    )

    def __init__(self):
        pass

    def stringToDict(self):
        pass

    def updateArtifact(self, operatorArtifact, field, item):
        operatorArtifact["data"][field].append(item)
        return operatorArtifact

    def build(self, strings):
        operatorArtifacts = self.operatorArtifactsTemplate
        for item in strings:
            operatorArtifacts = self.updateArtifact(operatorArtifacts, "customResourceDefinitions", yaml.load(item))
        print yaml.dump(operatorArtifacts)