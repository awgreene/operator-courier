import yaml as pyYaml
import command.identify as identify

class BuildCmd():
    name = 'build'
    
    def __init__(self):
        pass

    def __get_empty_bundle__(self):
        operatorArtifactsTemplate = dict(
            data = dict(
                customResourceDefinitions = [],
                clusterServiceVersions = [],
                packages = [],
            )
        )
        return operatorArtifactsTemplate
    
    def __get_field_entry__(self, yamlContent):
        yaml_type = identify.get_operator_artifact_type(yamlContent)
        if yaml_type == "ClusterServiceVersion" or yaml_type == "CustomResourceDefinition" or yaml_type == "Package":
            return yaml_type[0:1].lower() + yaml_type[1:] + 's'

    def __updateArtifact__(self, operatorArtifact, yamlContent):
        operatorArtifact["data"][self.__get_field_entry__(yamlContent)].append(pyYaml.load(yamlContent))
        return operatorArtifact

    def build_bundle(self, strings):
        bundle =  self.__get_empty_bundle__()
        for item in strings:
            bundle = self.__updateArtifact__(bundle, item)

        return bundle