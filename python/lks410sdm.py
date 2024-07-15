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
        Undefined = "UndefinedType"    # Undefined type, same as "Auto"
        NoStandard= f"{Object}{separator}NoStandard"
        Auto      = "Auto"    # Auto-detect type
        Null      = "Null"    # Null value (None in Python)

        all = [String, Integer8, Integer16, Integer, Integer32, Integer64, Float32, Float64, Boolean, List, Object, NoStandard, Auto, Null]
        primitive = [String, Integer8, Integer16, Integer, Integer32, Integer64, Float32, Float64, Boolean]
        complex = [List, Object, NoStandard]

    class Strings:
        Separators = ";;;"
        StandardVersion = "1.0"
        StandardHeader = f"LKS410 Standard Data Map"
        Standard = f"{StandardHeader}{Separators}{StandardVersion}{Separators}https://github.com/410-dev/lks410-sdm/tree/main/docs"
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
    def get(self, name: str):
        grandparent, parent, key, index = self.traverse(name, create_missing=False, allow_type_modifier=True)
        if parent is None:
            return None

        if index == -1:
            return parent.get(key)
        else:
            return parent[key][index] if index < len(parent[key]) else None

    def getExtraProperties(self) -> dict:
        return self.dictForm[Data.ReservedNames.ExtraProperties]

    def getRoot(self) -> dict:
        return self.dictForm[Data.ReservedNames.DataRoot]

    def set(self, name: str, value, setAs: str = Types.Auto, allowTypeModifier: bool = False) -> bool:
        grandparent, parent, key, index = self.traverse(name, create_missing=True, allow_type_modifier=allowTypeModifier)
        if parent is None:
            return False

        if index == -1:
            parent[key] = value
        else:
            parent[key][index] = value

        if setAs != Data.Types.Auto:
            parent[f"{key}.{Data.ReservedNames.TypeField}"] = setAs

        return True
    
    def setType(self, of: str, setAs: str):
        self.set(name=f"{of}.{Data.ReservedNames.TypeField}", value=setAs, allowTypeModifier=True)

    def has(self, name: str) -> bool:
        pass

    def info(self, name: str) -> tuple:
        return self.traverse(name, create_missing=False, allow_type_modifier=True)


    def typeOf(self, name: str) -> str:
        infodat = self.info(name)
        if infodat is None:
            return Data.Types.Undefined
        grandparent, parent, key, index = infodat
        if parent is None:
            return Data.Types.Undefined

        if index == -1:
            typeName = parent.get(f"{key}.{Data.ReservedNames.TypeField}", Data.Types.Undefined)
        else:
            typeName = parent[key][index].get(f"{Data.ReservedNames.TypeField}", Data.Types.Undefined) if index < len(parent[key]) else Data.Types.Undefined

        if typeName.startswith(Data.Types.NoStandard):
            typeClass: list = typeName.split(Data.Types.separator)[2:]
            found = False
            for typeClassName in typeClass:
                if typeClassName.startswith("@python="):
                    typeName = typeClassName.split("=")[1]
                    found = True
                    break

            if not found:
                typeName = Data.Types.Undefined

            typeName = f"{Data.Types.NoStandard}{Data.Types.separator}{typeName}"

        return typeName

    def typeMatches(self, name: str, typeName: str) -> bool:
        return self.typeOf(name) == typeName

    def remove(self, name: str) -> bool:
        grandparent, parent, key, index = self.traverse(name, create_missing=False, allow_type_modifier=True)
        if parent is None:
            return False

        if index == -1:
            if key in parent:
                del parent[key]
                return True
        else:
            if key in parent and index < len(parent[key]):
                parent[key][index] = None
                return True

        return False

    def parseFrom(self, stringData: str):
        jsonData = json.loads(stringData)
        if Data.ReservedNames.Standard not in jsonData:
            raise ValueError("Standard field not found in the data")
        stdString = jsonData[Data.ReservedNames.Standard]
        stdStringHeader = stdString.split(Data.Strings.Separators)[0]
        stdStringVersion = stdString.split(Data.Strings.Separators)[1]
        if stdStringHeader != Data.Strings.StandardHeader:
            raise ValueError("Standard header mismatch.")
        if stdStringVersion != Data.Strings.StandardVersion:
            print(f"Warning: Standard version mismatch. Expected {Data.Strings.StandardVersion}, got {stdStringVersion}")
        originalData = self.dictForm.copy()
        self.dictForm = jsonData
        invalidFields: list = self.checkFieldNameValidity()
        if len(invalidFields) > 0:
            self.dictForm = originalData
            raise ValueError("Field names are not valid: " + ", ".join(invalidFields))

    def compileString(self, linebreak: int = 4, checkFieldNameValidity: bool = True) -> str:
        if checkFieldNameValidity:
            results: list = self.checkFieldNameValidity()
            if len(results) > 0:
                raise ValueError("Field names are not valid: " + ", ".join(results))
        if linebreak < 0:
            return json.dumps(self.dictForm)
        return json.dumps(self.dictForm, indent=linebreak)

    def checkFieldNameValidity(self) -> list:
        fieldNames = Data.getKeyNamesRecursive(self.dictForm[Data.ReservedNames.DataRoot], "")
        invalidFieldNames = []
        reservedFieldNames = [Data.ReservedNames.Standard, Data.ReservedNames.DataRoot,
                              Data.ReservedNames.ExtraProperties, Data.ReservedNames.TypeField]
        for fieldName in fieldNames:
            if fieldName.split(".")[-1] in reservedFieldNames:
                invalidFieldNames.append(fieldName)
        return invalidFieldNames

    @staticmethod
    def getKeyNamesRecursive(obj: dict, currentScope: str) -> list:
        keyNames = []
        for key in obj:
            if key != Data.ReservedNames.TypeField and key.endswith(f".{Data.ReservedNames.TypeField}"):
                key = key.replace(f".{Data.ReservedNames.TypeField}", Data.Strings.TypeTemporaryString)
            keyNames.append(f"{currentScope}.{key}")
            if key not in obj:
                continue
            elif isinstance(obj[key], dict):
                keyNames += Data.getKeyNamesRecursive(obj[key], f"{currentScope}.{key}")
            elif isinstance(obj[key], list):
                for i in range(len(obj[key])):
                    if isinstance(obj[key][i], dict):
                        keyNames += Data.getKeyNamesRecursive(obj[key][i], f"{currentScope}.{key}[{i}]")
        for i in range(len(keyNames)):
            if keyNames[i][0] == ".":
                keyNames[i] = keyNames[i][1:]
        return keyNames

    def traverse(self, name: str, create_missing: bool = False, allow_type_modifier: bool = False):
        # Disallowed characters:
        disallowed_characters_for_key = ["{", "}", "(", ")", ":"]
        if not allow_type_modifier:
            disallowed_characters_for_key.append(f".{Data.ReservedNames.TypeField}")
        elif f".{Data.ReservedNames.TypeField}" in name:
            name = name.replace(f".{Data.ReservedNames.TypeField}", Data.Strings.TypeTemporaryString)

        for disallowed_character in disallowed_characters_for_key:
            if disallowed_character in name:
                return None, None, None, None

        # Nodes
        nodes_route = name.split(".")
        nodes_route_length = len(nodes_route)

        current_node = self.dictForm[Data.ReservedNames.DataRoot]
        parent_nodes = [current_node]
        final_key = nodes_route[-1]

        for i in range(nodes_route_length):
            current_node_name = nodes_route[i]
            list_access_idx = -1
            if "[" in current_node_name and "]" in current_node_name:
                list_access_idx = int(current_node_name.split("[")[1].split("]")[0])
                current_node_name = current_node_name.split("[")[0]

            if i == nodes_route_length - 1:
                if Data.Strings.TypeTemporaryString in current_node_name:
                    current_node_name = current_node_name.replace(Data.Strings.TypeTemporaryString,
                                                                  f".{Data.ReservedNames.TypeField}")

                if list_access_idx == -1:
                    return parent_nodes[-2] if len(parent_nodes) > 1 else None, parent_nodes[-1], current_node_name, -1
                else:
                    if create_missing and (current_node_name not in current_node or len(
                            current_node[current_node_name]) <= list_access_idx):
                        if current_node_name not in current_node:
                            current_node[current_node_name] = []
                        while len(current_node[current_node_name]) <= list_access_idx:
                            current_node[current_node_name].append(None)
                    return parent_nodes[-1], current_node, current_node_name, list_access_idx
            else:
                if create_missing and current_node_name not in current_node:
                    if list_access_idx == -1:
                        current_node[current_node_name] = {}
                    else:
                        current_node[current_node_name] = []
                        while len(current_node[current_node_name]) <= list_access_idx:
                            current_node[current_node_name].append(None)

                if current_node_name not in current_node:
                    return None, None, None, None

                if list_access_idx == -1:
                    current_node = current_node[current_node_name]
                else:
                    if list_access_idx >= len(current_node[current_node_name]):
                        return None, None, None, None
                    if current_node[current_node_name][list_access_idx] is None:
                        if create_missing:
                            current_node[current_node_name][list_access_idx] = {}
                        else:
                            return None, None, None, None
                    current_node = current_node[current_node_name][list_access_idx]
                parent_nodes.append(current_node)

        return None, None, None, None  # This line should never be reached, but it's here for completeness


