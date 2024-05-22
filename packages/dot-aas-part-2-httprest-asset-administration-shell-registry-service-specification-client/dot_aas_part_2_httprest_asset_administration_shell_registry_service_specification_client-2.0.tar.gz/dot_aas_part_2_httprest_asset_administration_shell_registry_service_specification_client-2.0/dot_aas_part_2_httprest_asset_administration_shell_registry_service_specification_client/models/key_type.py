from enum import Enum


class KeyType(str, Enum):
    ANNOTATEDRELATIONSHIPELEMENT = "AnnotatedRelationshipElement"
    ASSETADMINISTRATIONSHELL = "AssetAdministrationShell"
    BASICEVENTELEMENT = "BasicEventElement"
    BLOB = "Blob"
    CAPABILITY = "Capability"
    CONCEPTDESCRIPTION = "ConceptDescription"
    DATAELEMENT = "DataElement"
    ENTITY = "Entity"
    EVENTELEMENT = "EventElement"
    FILE = "File"
    FRAGMENTREFERENCE = "FragmentReference"
    GLOBALREFERENCE = "GlobalReference"
    IDENTIFIABLE = "Identifiable"
    MULTILANGUAGEPROPERTY = "MultiLanguageProperty"
    OPERATION = "Operation"
    PROPERTY = "Property"
    RANGE = "Range"
    REFERABLE = "Referable"
    REFERENCEELEMENT = "ReferenceElement"
    RELATIONSHIPELEMENT = "RelationshipElement"
    SUBMODEL = "Submodel"
    SUBMODELELEMENT = "SubmodelElement"
    SUBMODELELEMENTCOLLECTION = "SubmodelElementCollection"
    SUBMODELELEMENTLIST = "SubmodelElementList"

    def __str__(self) -> str:
        return str(self.value)
