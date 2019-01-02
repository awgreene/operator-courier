import yaml

def getOperatorArtifactType(operatorArtifactString):
    operatorArtifact = yaml.load(operatorArtifactString)
    if type(operatorArtifact) is dict:
        if "packageName" in operatorArtifact:
            return "packages"
        elif "kind" in operatorArtifact:
            if operatorArtifact["kind"] == "ClusterServiceVersion": 
                return "clusterServiceVersions"
            elif operatorArtifact["kind"] == "CustomResourceDefinition":
                return "customResourceDefinitions"
    return "invalid"