import json

class Data {

    Types = {
        String = "String"
        
        Integer8  = "Int8"  # byte in Java
        Integer16 = "Int16" # short in Java
        Integer   = "Int32" # int in Java
        Integer32 = "Int32"
        Integer64 = "Int64" # long in java
        

    }


    def __init__(self, checkValidity = True):
        self.checkValidity = checkValidity
        self.dictForm = {
            "standard": "LKS410 Standard Data Map;;;1.0;;;https://github.com/410-dev/lks410-std-dm/docs/README.md",
            "DataRoot": {},
            "ExtraProperties": {},
        }

    def get(self, name: str, getAs: str = "Auto"):
        pass

    def getExtraProperties(self) -> dict:
        pass

    def set(self, name: str, value, setAs: str = "Auto"): # If auto, don't include it
        pass
    
    def setType(self, of: str, setAs: str):
        pass

    def has(self, name: str) -> bool:
        pass

    def typeOf(self, name: str) -> str:
        pass

    def typeMatches(self, name: str, typeName: str) -> bool:
        pass

    def remove(self, name: str, onlyIfNotExist: bool = False) -> bool:
        pass
    
    def parseFrom(self, stringData: str) -> self:
        pass
    
    def compileJson(self) -> dict:
        pass

    def compileString(self) -> str:
        pass

    def checkFieldNameValidity(self) -> bool:
        pass
}
