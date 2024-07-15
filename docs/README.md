# LKS410 Standard Data Map Structure Documentation

## Overview

The LKS410 Standard Data Map is a structured data format designed for efficient data storage, retrieval, and cross-language compatibility. It provides a standardized way to represent various data types, including primitive types, lists, and custom objects, with a focus on Java and Python interoperability.


## Code Implementation
[Python](Python.md) / [Java](Java.md) (Not ready)

## Structure

The LKS410 Standard Data Map consists of three main components:

1. Standard String
2. DataRoot
3. ExtraProperties

### 1. Standard String

```json
"standard": "LKS410 Standard Data Map;;;1.0;;;https://github.com/410-dev/lks410-sdm/tree/main/docs"
```

- **Purpose**: The standard string is used for checking compatibility between different implementations or versions of the LKS410 Standard.
- **Format**: It consists of three parts separated by `;;;`:
  1. The name of the standard ("LKS410 Standard Data Map")
  2. The version number ("1.0")
  3. A URL to the documentation

### 2. DataRoot

The `DataRoot` is the main container for all the data stored in the structure. It's represented as a JSON object where each key-value pair represents a data item.

#### Data Item Format

Each data item in the `DataRoot` consists of two parts:

1. The value itself
2. A type definition (Optional)

For example:
```json
"val1": "string data",
"val1.type": "String"
```

Note: Type implementation is not mandatory. The .type suffix for defining types is optional and can be omitted if type specification is not needed for a particular use case. Auto, Undefined types will be automatically ommited when compiling to JSON.

#### Supported Types

1. **Primitive Types**:
   - `String`: For text data
   - `Integer32`: For 32-bit integers
   - `Integer64`: For 64-bit integers
   - `Boolean`: For true/false values
   - `Float64`: For 64-bit floating-point numbers

2. **List Types**:
   - `List:String`: A list of strings
   - `List:Auto`: A list of mixed types

3. **Object Types**:
   - `Object:NoStandard`: For custom objects with language-specific implementations

4. **Auto Type**:
   - `Auto`: For automatic type inference

#### Type Specifications

- **Lists**: Use `List:<ElementType>` to specify the type of elements in the list.
  Example: `"val4.type": "List:String"`

- **Custom Objects**: Use `Object:NoStandard:@<language>=<full.class.path>` to specify language-specific object types.
  Example: `"val6.type": "Object:NoStandard:@python=framework.objects.UserObject:@java=javax.randomframework.objects.UserObject"`


Raw binary data is not supported in this section.

### 3. ExtraProperties

The `ExtraProperties` section is designed for storing miscellaneous data that doesn't fit into the main `DataRoot` structure.

- It's represented as a JSON object.
- The library provides access to this entire object but doesn't offer specific methods for manipulating its contents.
- Raw binary data is not supported in this section.

## Example Structure

```json
{
    "standard": "LKS410 Standard Data Map;;;1.0;;;https://github.com/410-dev/lks410-sdm/tree/main/docs",
    "DataRoot": {
        "val1": "string data",
        "val1.type": "String",

        "val2": 1,

        "val3": 1,
        "val3.type": "Integer64",

        "val4": ["Hello World"],
        "val4.type": "List:String",

        "val5": ["Hello World", 123],
        "val5.type": "List:Auto",

        "val6": {
            "name": "John Smith",
            "phone": "1234-1234"
        },
        "val6.type": "Object:NoStandard:@python=framework.objects.UserObject:@java=javax.randomframework.objects.UserObject",

        "val7": true,

        "val8": 0.4,
        "val8.type": "Float64",

        "val9": "Hello"
    },
    "ExtraProperties": {
    }
}
```

## Usage Guidelines

1. **Consistency**: Always include the standard string for compatibility checking.
2. **Type Definitions**: For each value in `DataRoot`, always provide a corresponding type definition using the `.type` suffix.
3. **Custom Objects**: When using custom objects, ensure that the specified classes exist in your project for proper deserialization.
4. **ExtraProperties**: Use this section sparingly and only for data that doesn't fit the structured format of `DataRoot`.
5. **Language Interoperability**: When working across different programming languages, pay special attention to the type definitions to ensure proper data conversion.

## Best Practices

1. **Version Control**: Keep track of changes to your data structure and update the version number in the standard string accordingly.
2. **Documentation**: Maintain clear documentation for any custom objects or specific usages of `ExtraProperties`.
3. **Type Safety**: Leverage the type system to ensure data integrity across different parts of your application.
4. **Validation**: Implement validation checks to ensure that the data adheres to the expected structure and types.

By following this structure and guidelines, you can create robust, interoperable data representations that work seamlessly across different programming environments, particularly Java and Python.