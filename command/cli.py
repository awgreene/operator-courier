import yaml
from command.build import BuildCmd
from command.push import PushCmd
from command.validate import ValidateCmd

def all_commands():
    return {
        BuildCmd.name: BuildCmd,
        PushCmd.name: PushCmd,
        ValidateCmd.name: ValidateCmd,
    }

item0 = '''
apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
metadata:
  name: marketplace-operator.v0.0.1
  namespace: placeholder
spec:
  displayName: marketplace-operator
  description: |-
    Marketplace is a gateway for users to consume off-cluster Operators which will include Red Hat, ISV, optional OpenShift and community content.
  keywords: ['marketplace', 'catalog', 'olm', 'admin']
  version: 0.0.1
  maturity: alpha
  maintainers:
  - name: AOS Marketplace Team
    email: aos-marketplace@redhat.com
  provider:
    name: Red Hat
  labels:
    name: marketplace-operator
  selector:
    matchLabels:
      name: marketplace-operator
  links:
  - name: Markplace Operator Source Code
    url: https://github.com/operator-framework/operator-marketplace
  install:
    strategy: deployment
    spec:
      clusterPermissions:
      - serviceAccountName: marketplace-operator
        rules:
        - apiGroups:
          - marketplace.redhat.com
          resources:
          - "*"
          verbs:
          - "*"
        - apiGroups:
          - ""
          resources:
          - services
          - configmaps
          verbs:
          - "*"
        - apiGroups:
          - operators.coreos.com
          resources:
          - catalogsources
          verbs:
          - "*"
      deployments:
      - name: marketplace-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              name: marketplace-operator
          template:
            metadata:
              name: marketplace-operator
              labels:
                name: marketplace-operator
            spec:
              serviceAccountName: marketplace-operator
              containers:
                - name: marketplace-operator
                  image: quay.io/openshift/origin-operator-marketplace:latest
                  ports:
                  - containerPort: 60000
                    name: metrics
                  - containerPort: 8080
                    name: healthz
                  command:
                  - marketplace-operator
                  imagePullPolicy: Always
                  livenessProbe:
                    httpGet:
                      path: /healthz
                      port: 8080
                  readinessProbe:
                    httpGet:
                      path: /healthz
                      port: 8080
                  env:
                    - name: WATCH_NAMESPACE
                      valueFrom:
                        fieldRef:
                          fieldPath: metadata.namespace
                    - name: OPERATOR_NAME
                      value: "marketplace-operator"
  customresourcedefinitions:
    owned:
    - name: operatorsources.marketplace.redhat.com
      version: v1alpha1
      kind: OperatorSource
      displayName: Operator Source
      description: Represents an OperatorSource.
      specDescriptors: 
        - description: The type of the operator source.
          displayName: Type
          path: type
        - description: Points to the remote app registry server from where operator manifests can be fetched.
          displayName: Endpoint
          path: endpoint
        - description: |-
            The namespace in app registry.
            Only operator manifests under this namespace will be visible.
            Please note that this is not a k8s namespace.
          displayName: Registry Namespace
          path: registryNamespace
      statusDescriptors:
        - description: Current status of the CatalogSourceConfig
          displayName: Current Phase Name
          path: currentPhase.phase.name
        - description: Message associated with the current status
          displayName: Current Phase Message
          path: currentPhase.phase.message
    - name: catalogsourceconfigs.marketplace.redhat.com
      version: v1alpha1
      kind: CatalogSourceConfig
      displayName: Catalog Source Config
      description: Represents a CatalogSourceConfig object which is used to configure a CatalogSource.
      specDescriptors:
        - description: The namespace where the operators will be enabled.
          displayName: Target Namespace
          path: targetNamespace
        - description: List of operator(s) which will be enabled in the target namespace
          displayName: Packages
          path: packages
      statusDescriptors:
        - description: Current status of the CatalogSourceConfig
          displayName: Current Phase Name
          path: currentPhase.phase.name
        - description: Message associated with the current status
          displayName: Current Phase Message
          path: currentPhase.phase.message
'''

item1 = '''
packageName: marketplace
channels:
- name: alpha
  currentCSV: marketplace-operator.v0.0.1
'''

item2 = '''
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: operatorsources.marketplace.redhat.com
  annotations:
    displayName: Operator Source
    description: Represents an OperatorSource.
spec:
  group: marketplace.redhat.com
  names:
    kind: OperatorSource
    listKind: OperatorSourceList
    plural: operatorsources
    singular: operatorsource
    shortNames:
    - opsrc
  scope: Namespaced
  version: v1alpha1
  additionalPrinterColumns:
  - name: Type
    type: string
    description: The type of the OperatorSource
    JSONPath: .spec.type
  - name: Endpoint
    type: string
    description: The endpoint of the OperatorSource
    JSONPath: .spec.endpoint
  - name: Registry
    type: string
    description: App registry namespace
    JSONPath: .spec.registryNamespace
  - name: Status
    type: string
    description: Current status of the OperatorSource
    JSONPath: .status.currentPhase.phase.name
  - name: Message
    type: string
    description: Message associated with the current status
    JSONPath: .status.currentPhase.phase.message
  - name: Age
    type: date
    JSONPath: .metadata.creationTimestamp
  validation:
    openAPIV3Schema:
      properties:
        spec:
          type: object
          description: Spec for an OperatorSource.
          required:
          - type
          - endpoint
          - registryNamespace
          properties:
            type:
              type: string
              description: The type of the OperatorSource
              pattern: 'appregistry'
            endpoint:
              type: string
              description: Points to the remote app registry server from where operator manifests can be fetched.
            registryNamespace:
              type: string
              description: |-
                The namespace in app registry.
                Only operator manifests under this namespace will be visible.
                Please note that this is not a k8s namespace.
'''
item3 = '''
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: catalogsourceconfigs.marketplace.redhat.com
  annotations:
    displayName: Catalog Source Config
    description: Represents a CatalogSourceConfig.
spec:
  group: marketplace.redhat.com
  names:
    kind: CatalogSourceConfig
    listKind: CatalogSourceConfigList
    plural: catalogsourceconfigs
    singular: catalogsourceconfig
    shortNames:
    - csc
  scope: Namespaced
  version: v1alpha1
  additionalPrinterColumns:
  - name: TargetNamespace
    type: string
    description: The namespace where the operators will be enabled
    JSONPath: .spec.targetNamespace
  - name: Packages
    type: string
    description: List of operator(s) which will be enabled in the target namespace
    JSONPath: .spec.packages
  - name: Status
    type: string
    description: Current status of the CatalogSourceConfig
    JSONPath: .status.currentPhase.phase.name
  - name: Message
    type: string
    description: Message associated with the current status
    JSONPath: .status.currentPhase.phase.message
  - name: Age
    type: date
    JSONPath: .metadata.creationTimestamp
  validation:
    openAPIV3Schema:
      properties:
        spec:
          type: object
          description: Spec for a CatalogSourceConfig
          required:
          - targetNamespace
          - packages
          properties:
            targetNamespace:
              type: string
              description: The namespace where the operators will be enabled
            packages:
              type: string
              description: Comma separated list of operator(s) without spaces which will be enabled in the target namespace
'''
def main():
  #print(item)
  BuildCmd().build([item0, item1, item2, item3])
  #PushCmd().push()
  #ValidateCmd().validate()
  #print yaml.dump(yaml.load(document))
