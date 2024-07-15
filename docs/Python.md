# LKS410 Standard Data Map Controller Library Documentation for Python

## Overview

This is a documentation for LKS410 SDM (Standard Data Map) controller library for Python and its implementation.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Data Types](#data-types)
4. [Main Methods](#main-methods)
5. [Advanced Features](#advanced-features)
6. [Examples](#examples)

## Installation

To use this library, include the `Data` class in your Python project.

## Basic Usage

### Creating a Data Object

```python
from data_class import Data

# Create an empty Data object
data = Data()

# Create a Data object from a JSON string
with open('/path/to/json', 'r') as f:
    data = Data(parseString=f.read())
```

### Setting Values

```python
data.set("user.name", "John Doe")
data.set("user.age", 30)
data.set("user.scores", [85, 90, 95])
```

### Getting Values

```python
name = data.get("user.name")
age = data.get("user.age")
scores = data.get("user.scores")
```

### Removing Values

```python
data.remove("user.age")
```

## Data Types

The library supports various data types, defined in `Data.Types`. These types are designed to be compatible with Java data types and provide flexibility for complex data structures.

### Basic Types

- `String`
- `Integer8`, `Integer16`, `Integer`, `Integer32`, `Integer64`
- `Float32`, `Float64`
- `Boolean`
- `List`
- `Object`
- `Undefined` / `NoStandard` / `Auto`
- `Null`

### Complex Type Specifications

The library allows for more detailed type specifications, especially useful for Java compatibility:

#### List Types

You can specify the type of elements in a list using the following format:

```
List:<ElementType>
```

Examples:
- `List:String`: A list of strings
- `List:Auto`: A list of mixed types (will be casted to `java.lang.Object` in Java)
- `List:Float64`: A list of 64-bit floating-point numbers

In Java, these will be casted to appropriate `ArrayList<T>` types.

#### Non-Standard Object Types

For custom objects or objects that require specific handling in different languages, you can use the `Object:NoStandard` type with additional specifications:

```
Object:NoStandard:@<language>=<full.class.path>
```

Example:
```
Object:NoStandard:@python=framework.objects.UserObject:@java=javax.randomframework.objects.UserObject
```

This specifies that:
- In Python, this object should be handled as `framework.objects.UserObject`
- In Java, it should be casted to `javax.randomframework.objects.UserObject`

### Setting Types

You can specify these complex types when setting a value:

```python
data.set("users", [], setAs="List:String")
data.set("scores", [85.5, 90.0, 95.5], setAs="List:Float64")
data.set("customObject", some_object, setAs="Object:NoStandard:@python=framework.objects.UserObject:@java=javax.randomframework.objects.UserObject")
```

### Checking Types

```python
type_of_users = data.typeOf("users")  # Returns "List:String"
is_float_list = data.typeMatches("scores", "List:Float64")
```

## Main Methods

- `set(name, value, setAs=Types.Auto, allowTypeModifier=False)`: Set a value in the data structure.
- `get(name)`: Retrieve a value from the data structure.
- `remove(name)`: Remove a value from the data structure.
- `has(name)`: Check if a value exists in the data structure.
- `typeOf(name)`: Get the type of a value.
- `typeMatches(name, typeName)`: Check if a value's type matches the specified type.
- `info(name)`: Get detailed information about a node in the data structure.

## Advanced Features

### Parsing and Compiling

- `parseFrom(stringData)`: Parse a JSON string into the data structure.
- `compileString(linebreak=4, checkFieldNameValidity=True)`: Compile the data structure into a JSON string.

### Extra Properties

- `getExtraProperties()`: Get additional properties not part of the main data structure.
- `getRoot()`: Get the root of the data structure.

### Type Modification

- `setType(of, setAs)`: Set the type of a specific field.

## Examples

### Creating a Complex Structure

```python
data = Data()
data.set("company.name", "TechCorp")
data.set("company.founded", 1995)
data.set("company.employees", [
    {"name": "Alice", "role": "Developer"},
    {"name": "Bob", "role": "Designer"}
])

print(data.compileString())
```

### Type Checking and Validation

```python
data.set("product.price", 19.99, setAs=Data.Types.Float32)
data.set("product.inStock", True, setAs=Data.Types.Boolean)

print(data.typeOf("product.price"))  # Output: Float32
print(data.typeMatches("product.inStock", Data.Types.Boolean))  # Output: True
```

### Using List Indexing

```python
data.set("scores[0]", 85)
data.set("scores[1]", 90)
data.set("scores[2]", 95)

print(data.get("scores"))  # Output: [85, 90, 95]
```

