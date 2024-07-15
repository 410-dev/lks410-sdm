import json

class Data:

    class Types:
        separator = ":"
        String    = "String"
        Integer8  = "Int8"    # byte in Java
        Integer16 = "Int16"   # short in Java
        Integer   = "Int32"   # int in Java
        Integer32 = "Int32"
        Integer64 = "Int64"   # long in java
        Float32   = "Float32" # float in Java
        Float64   = "Float64" # double in Java
        Boolean   = "Boolean" # boolean in Java
        List      = "List"
        Object    = "Object"  # Json object in Java
        Undefined = "NoStandard"    # Undefined type, same as "Auto"
        NoStandard= f"{Object}{separator}{Undefined}" # No standard type, same as "Auto
        Auto      = "Auto"    # Auto-detect type
        Null      = "Null"    # Null value (None in Python)

        all = [String, Integer8, Integer16, Integer, Integer32, Integer64, Float32, Float64, Boolean, List, Object, NoStandard, Auto, Null]
        primitive = [String, Integer8, Integer16, Integer, Integer32, Integer64, Float32, Float64, Boolean]
        complex = [List, Object, NoStandard]

    class Strings:
        Standard = "LKS410 Standard Data Map;;;1.0;;;https://github.com/410-dev/lks410-std-dm/docs/README.md"
        TypeTemporaryString = "__TYPE__"

    class ReservedNames:
        Standard = "standard"
        DataRoot = "DataRoot"
        ExtraProperties = "ExtraProperties"
        TypeField = "type"

    def __init__(self, parseString: str = None, checkValidity: bool = True):
        self.checkValidity = checkValidity
        self.dictForm = {
            Data.ReservedNames.Standard: Data.Strings.Standard,
            Data.ReservedNames.DataRoot: {},
            Data.ReservedNames.ExtraProperties: {}
        }

        if parseString is not None:
            self.parseFrom(parseString)



    # This will get data from the object, if it exists
    # This runs recursively
    # It should return parent node if it is the last node, so that type can be checked
    def get(self, name: str, defaultValue=None, recursion_fromObject=None, recursion_nodesToGo:list = None, recursion_depth:int = 0, querySafeMode: bool = False, setIfNotFound = False): # Unless recursion depth = 0, it should be (value, type, parent)
        # If recursion_nodesToGo is None, it means that this is the first call
        if recursion_nodesToGo is None:
            recursion_nodesToGo = name.split(".")

        # If recursion_fromObject is None, it means that this is the first call
        if recursion_fromObject is None:
            recursion_fromObject = self.dictForm[Data.ReservedNames.DataRoot]

        iterableObject = recursion_fromObject

        # For each node, run recursion. If found, return it
        supportedRecursionTypes = [Data.Types.Auto, Data.Types.Object, Data.Types.NoStandard, Data.Types.List]

        # If the key is a list access, split the key and get the index
        listAccessIdx = -1
        if "[" in recursion_nodesToGo[0] and "]" in recursion_nodesToGo[0]:
            listAccessIdx = int(recursion_nodesToGo[0].split("[")[1].split("]")[0])
            recursion_nodesToGo[0] = recursion_nodesToGo[0].split("[")[0]

        result: tuple = (None, None, None)
        for key in iterableObject.keys():

            # If the node is found, return it
            if recursion_nodesToGo[0] == key and len(recursion_nodesToGo) == 1:

                # Non-list access
                if listAccessIdx == -1:
                    if f"{key}.{Data.ReservedNames.TypeField}" in iterableObject:
                        result = (iterableObject[key], iterableObject[f"{key}.{Data.ReservedNames.TypeField}"], iterableObject)
                    else:
                        result = (iterableObject[key], Data.Types.Auto, iterableObject)
                    break

                # List access
                else:
                    if f"{key}.{Data.ReservedNames.TypeField}" in iterableObject:
                        if len(iterableObject[key]) > listAccessIdx and querySafeMode:
                            result = (iterableObject[key], iterableObject[f"{key}.{Data.ReservedNames.TypeField}"], iterableObject)
                        else:
                            result = (iterableObject[key][listAccessIdx], iterableObject[f"{key}.{Data.ReservedNames.TypeField}"], iterableObject)
                    else:
                        if len(iterableObject[key]) > listAccessIdx and querySafeMode:
                            result = (iterableObject[key], Data.Types.Auto, iterableObject)
                        else:
                            result = (iterableObject[key][listAccessIdx], Data.Types.Auto, iterableObject)
                    break

            # Run type checking. This allows to skip the type checking if the type is not specified
            elif (
                    type(recursion_fromObject[key]) is dict
                    and
                    (
                            (f"{key}.{Data.ReservedNames.TypeField}" not in iterableObject)
                            or
                            (f"{key}.{Data.ReservedNames.TypeField}" in iterableObject and iterableObject[f"{key}.{Data.ReservedNames.TypeField}"] in supportedRecursionTypes)
                    )
            ):
                if recursion_nodesToGo[0] == key:
                    if listAccessIdx == -1:
                        result = self.get(name, defaultValue, recursion_fromObject[key], recursion_nodesToGo[1:], recursion_depth + 1, querySafeMode)
                    else:
                        result = self.get(name, defaultValue, recursion_fromObject[key][listAccessIdx], recursion_nodesToGo[1:], recursion_depth + 1, querySafeMode)
                    break

            # Not found
            else:
                continue

        if recursion_depth == 0:
            if defaultValue is not None and result[0] is None:
                if setIfNotFound:
                    self.set(name, defaultValue)
                return defaultValue
            return result[0]

        return result

    def getExtraProperties(self) -> dict:
        return self.dictForm[Data.ReservedNames.ExtraProperties]

    def getRoot(self) -> dict:
        return self.dictForm[Data.ReservedNames.DataRoot]

    def set(self, name: str, value, setAs: str = Types.Auto, allowTypeModifier: bool = False) -> bool: # If auto, don't include type data
        # Disallowed characters:
        disallowedCharactersForKey = ["{", "}", "(", ")", ":"]
        if not allowTypeModifier:
            disallowedCharactersForKey.append(f".{Data.ReservedNames.TypeField}")
        elif f".{Data.ReservedNames.TypeField}" in name:
            name = name.replace(f".{Data.ReservedNames.TypeField}", Data.Strings.TypeTemporaryString)
        for disallowedCharacter in disallowedCharactersForKey:
            if disallowedCharacter in name:
                return False

        # If the type is invalid, return False
        if setAs not in Data.Types.all:
            return False

        # Nodes
        nodesRoute = name.split(".")
        nodesRouteLength = len(nodesRoute)

        currentNode = self.dictForm[Data.ReservedNames.DataRoot]
        parentNodes = [currentNode]

        for i in range(nodesRouteLength):
            currentNodeName = nodesRoute[i]
            listAccessIdx = -1
            if "[" in currentNodeName and "]" in currentNodeName:
                listAccessIdx = int(currentNodeName.split("[")[1].split("]")[0])
                currentNodeName = currentNodeName.split("[")[0]

            if i == nodesRouteLength - 1:
                if listAccessIdx == -1:
                    if Data.Strings.TypeTemporaryString in currentNodeName:
                        currentNodeName = currentNodeName.replace(Data.Strings.TypeTemporaryString, f".{Data.ReservedNames.TypeField}")
                    currentNode[currentNodeName] = value
                else:
                    if currentNodeName not in currentNode:
                        currentNode[currentNodeName] = []
                    while len(currentNode[currentNodeName]) <= listAccessIdx:
                        currentNode[currentNodeName].append(None)
                    currentNode[currentNodeName][listAccessIdx] = value
                if setAs != Data.Types.Auto:
                    currentNode[f"{currentNodeName}.{Data.ReservedNames.TypeField}"] = setAs
            else:
                if currentNodeName not in currentNode:
                    if listAccessIdx == -1:
                        currentNode[currentNodeName] = {}
                    else:
                        currentNode[currentNodeName] = []
                        while len(currentNode[currentNodeName]) <= listAccessIdx:
                            currentNode[currentNodeName].append(None)  # Changed from {} to None

                if listAccessIdx == -1:
                    currentNode = currentNode[currentNodeName]
                else:
                    if currentNode[currentNodeName][listAccessIdx] is None:
                        currentNode[currentNodeName][listAccessIdx] = {}  # Initialize with {} only when accessing
                    currentNode = currentNode[currentNodeName][listAccessIdx]
                parentNodes.append(currentNode)

        return True
    
    def setType(self, of: str, setAs: str):
        self.set(name=f"{of}.{Data.ReservedNames.TypeField}", value=setAs, allowTypeModifier=True)

    def has(self, name: str) -> bool:
        pass

    def info(self, name: str) -> tuple:
        return self.get(name, recursion_fromObject=self.dictForm[Data.ReservedNames.DataRoot], recursion_depth=1, querySafeMode=True)

    def typeOf(self, name: str) -> str:
        print(self.info(name))
        typeInfo = self.info(f"{name}.{Data.ReservedNames}")[1]
        if typeInfo is None:
            return Data.Types.Auto
        return typeInfo

    def typeMatches(self, name: str, typeName: str) -> bool:
        return self.typeOf(name) == typeName

    def remove(self, name: str, onlyIfNotExist: bool = False) -> bool:
        pass
    
    def parseFrom(self, stringData: str):
        jsonData = json.loads(stringData)
        self.dictForm = jsonData

    def compileString(self, linebreak: int = 4, checkFieldNameValidity: bool = True) -> str:
        if checkFieldNameValidity:
            results: list = self.checkFieldNameValidity()
            if len(results) > 0:
                raise ValueError("Field names are not valid: " + ", ".join(results))
        if linebreak < 0:
            return json.dumps(self.dictForm)
        return json.dumps(self.dictForm, indent=linebreak)

    def checkFieldNameValidity(self) -> list:
        # Return result of the check - invalid field names
        return []




stringd = """{
    "standard": "LKS410 Standard Data Map;;;1.0;;;https://github.com/410-dev/lks410-std-dm/docs/README.md",
    "DataRoot": {
        "val1": "string data",
        "val1.type": "String",

        "val2": 1,
        "val2.type": "Integer32",

        "val3": 1,
        "val3.type": "Integer64",

        "val4": ["Hello World"],
        "val4.type": "List:String",

        "val5": ["Hello World", 123],
        "val5.type": "List:Any",

        "val6": {
            "name": "John Appleseed",
            "phone": "1234-1234"
        },
        "val6.type": "Object",

        "val7": true,
        "val7.type": "Boolean",

        "val8": 0.4,
        "val8.type": "Float:double",

        "val9": "Hello",
        "val9.type": "Auto"
    },
    "ExtraProperties": {

    }
}"""

data = Data(parseString=stringd)

data.set("val64.val32.val8.lines[1].test[4].line", "Hello World", Data.Types.Integer16)
# print(data.get("val64.val32.val8.lines[1].test[4].line"))
# print(data.typeOf("val64.val32.val8.lines[1].test[4].line"))
# data.setType("val64.val32.val8.lines[1].test[4].line", Data.Types.String)
# print(data.typeOf("val64.val32.val8.lines[1].test[4].line"))
print(data.compileString())

