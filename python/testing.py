from lks410sdm import Data
from sampleObjects.user import UserObject

sd = """
{
    "standard": "LKS410 Standard Data Map;;;1.0;;;https://github.com/410-dev/lks410-sdm/tree/main/docs",
    "DataRoot": {
        "val1": "string data",
        "val1.type": "String",

        "val2": 1,

        "val3": 1,
        "val3.type": "Int64",

        "Val4": ["Hello World"],
        "Val4.type": "List:String",

        "Val5": ["Hello World", {"id": "hello"}],
        "Val5.type": "List:Auto",

        "Val6": {
            "name": "John Smith",
            "phone": "1234-1234",
            "email": "johnsmith@company.com"
        },
        "Val6.type": "Object:NoStandard:@python=sampleObjects.user.UserObject:@java=javax.randomframework.objects.UserObject",

        "void": true,

        "val8": 0.4,
        "val8.type": "Float64",

        "val9": "Hello"
    },
    "ExtraProperties": {}
}
"""

d = Data(parseString=sd)
print(d.compileString())
uo = UserObject(None, None, None)
d.set("User", uo)
success = d.typeCheck()
d.sortKeysByName()
d.append("Val4", "988rugpwefir90jgpjpwdfoigjpsdfo")
print(d.compileString())
print(success)
