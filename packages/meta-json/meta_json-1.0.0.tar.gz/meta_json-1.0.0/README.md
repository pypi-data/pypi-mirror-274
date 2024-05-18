# meta_json

Given a JSON response as a dictionary, extract the metadata such as its structure and data model. 


## Introduction

This package is intended to help with JSON analysis by extracting its metadata and ease the data modeling tasks regularly used in design of databases, data catalogs, data warehouses, APIs, etc. 


## Installation

This package is available in PyPI and GitHub. Just run:

```python
  pip install meta-json
```

Or clone the repository:

```console
  git clone https://github.com/juangcr/meta_json.git 
  cd meta_json
  python setup.py install
```

## Usage

```python
  from meta_json import MetaJson
  
  your_json_data_as_dict = {
    "name": "John Doe",
    "contact": "john_doe@mail.net",
    "status": {
      "start_date": "1970-01-01",
      "active": "true",
      "credits": {
        "due": 10,
        "remaining": 90
        }
    }
  }

  meta = MetaJson(your_json_data_as_dict)
  
  meta.types()  # Returns every data type available.
```

```console
  {
    "name": "str",
    "contact": "str", 
    "status": {
      "start_date": "datetime",
      "active": "str",
      "credits": {
        "due": "int",
        "remaining": "int"
        }
    }
  }
```

Keep in mind that the datetime recognition supports the following patterns:

- YYYY-MM-DD
- YYYY/MM/DD
- DD-MM-YYYY
- DD/MM/YYYY
- MM-DD-YYYY
- MM/DD/YYYY

```python
  meta.attributes()  # Returns a list with two elements: the grouped main keys
                   # and the rest of the subkeys alltogether.
```

```console
  [
    [
      "name",
      "contact",
      "status"
    ],
    [
      "start_date",
      "active",
      "credits",
      "due",
      "remaining"
    ]
  ]
```

```python
  meta.layers()  # Returns all keys grouped by layer depth.
```

```console
  {
    "layer_0" :[
      "name",
      "contact",
      "status"
    ],
    "layer_1": [
      "start_date",
      "active",
      "credits"
    ],
    "layer_2": [
      "due",
      "remaining"
    ]
  ]
```

