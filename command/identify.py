import yaml

def getOperatorArtifactType(operatorArtifactString):
    operatorArtifact = yaml.load(operatorArtifactString)
    if operatorArtifact.has_key("packageName"):
        return "packages"
    elif operatorArtifact["kind"] == "ClusterServiceVersion": 
        return "clusterServiceVersions"
    elif operatorArtifact["kind"] == "CustomResourceDefinition":
        return "customResourceDefinitions"
    else:
        # TODO: Throw Error
        pass
