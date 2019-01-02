import yaml
import command.identify as id

class BuildCmd():
    name = 'build'
    #TODO: Add const
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
        operatorArtifact["data"][field].append(yaml.load(item))
        return operatorArtifact



    def build(self, strings):
        operatorArtifacts = self.operatorArtifactsTemplate
        for item in strings:
            operatorArtifacts = self.updateArtifact(operatorArtifacts, id.getOperatorArtifactType(item), item)
        
        print(yaml.dump(operatorArtifacts))
