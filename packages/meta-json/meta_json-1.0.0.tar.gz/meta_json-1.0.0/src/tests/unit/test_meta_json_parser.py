import pytest
from meta_json.attribute_parser import AttributesParser
from meta_json.layer_parser import LayersParser
from meta_json.type_parser import TypesParser


"""Read the TESTING.md document for more information."""

EXAMPLE_1 = [
	"item_1",
    "item_2",
	["item_3", "item_4", "item_5"],
    [["item_6"]],
	[[], [], []],
	[], 
    ]


EXAMPLE_2 = {
	"name": "John Doe",
	"height": 1.73,
	"mass": 77,
	"hair_color": "blond",
	"skin_color": "fair",
	"eye_color": "blue",
	"birth_year": "1970",
	"gender": "male",
	"species": ["Human"],
	"created": "2023-03-09T13:50:41.674000Z",
	"edited": "2023-03-20T21:17:53.791000Z",
	"url": "https://www.url.dev"
}


EXAMPLE_3 = {
    "layer1_a": "text",
    "layer1_b": 3.14,
    "layer1_c": {
        "layer2_a": 42,
        "layer2_b": "more text"
        },
    "layer1_d": ["bit", "more", "text"],
    "layer1_e": {
        "layer2_c": [
            {"layer3_a": "deep"},
            {"layer3_b": "deeper"}
            ],
        "layer2_d": {
            "layer3_c": {"layer4_a": "deepest"}
        }
    }
}


def test_datetimes():
    data = [
	    "2014-12-19T13:50:51.644000Z",
	    "2014/12/20 21:17:56",
	    "21-12-2014 22:54:00",
	    "22/12/2014",
	    "12-23-2014 12:34:56 EST",
	    "12/24/2014",
	    "https://api.dev/api/1/"
        ]

    meta = TypesParser()
    results = [meta._parse_datetimes(d) for d in data]
    assert results == [True, True, True, True, True, True, False] 


def test_flat_list():
    output_data = [
	    "item_1",
	    "item_2",
	    "item_3",
	    "item_4",
	    "item_5",
	    "item_6"
        ]

    meta = AttributesParser()
    result = meta._hard_flatten(EXAMPLE_1)
    assert result == output_data 


def test_flat_empty_list():
    meta = AttributesParser()
    result = meta._hard_flatten([])
    assert result == []


def test_partial_flat_list():
    output_data = [
	    "item_1",
        "item_2",
	    "item_3",
	    "item_4",
	    "item_5",
        ["item_6"],
        [],
	    [],
	    [], 
        ]

    meta = LayersParser()
    result = meta._soft_flatten(EXAMPLE_1)
    assert result == output_data 


def test_partial_flat_empty_list():
    meta = LayersParser()
    result = meta._soft_flatten([])
    assert result == []


def test_types_one_layer():
    output_data = {
		"name": "str",
	    "height": "float",
	    "mass": "int",
	    "hair_color": "str",
	    "skin_color": "str",
	    "eye_color": "str",
	    "birth_year": "str",
	    "gender": "str",
	    "species": ["str"],
    	"created": "datetime",
	    "edited": "datetime",
    	"url": "str" 
    }

    meta = TypesParser()
    meta_types = meta.type_parser(EXAMPLE_2)
    assert meta_types == output_data


def test_types_empty():
    meta = TypesParser()
    meta_types = meta.type_parser({})
    assert meta_types == {}


def test_attribute_one_layer():
    output_data = [[
		"name",
	    "height",
	    "mass",
	    "hair_color",
	    "skin_color",
	    "eye_color",
	    "birth_year",
	    "gender",
	    "species",
    	"created",
	    "edited",
    	"url" 
        ], []]

    meta = AttributesParser()
    meta_attr = meta.attribute_parser(EXAMPLE_2)
    assert meta_attr == output_data


def test_attributes_multiple_layers():
    output_data = [
            [
                "layer1_a",
                "layer1_b",
                "layer1_c",
                "layer1_d",
                "layer1_e",
                ],
            [
                'layer2_a',
                'layer2_b',
                'layer2_c',
                'layer2_d',
                'layer3_a',
                'layer3_b',
                'layer3_c',
                'layer4_a'
                ]
            ]

    meta = AttributesParser()
    meta_attr = meta.attribute_parser(EXAMPLE_3)
    assert meta_attr == output_data


def test_attribute_empty():
    meta = AttributesParser()
    meta_attr = meta.attribute_parser({})
    assert meta_attr == [[], []]


def test_layer_parser():
    output_data = [ 
            ["layer1_a", []],
            ["layer1_b", []],
            ["layer1_c",  [["layer2_a", []], ["layer2_b", []]]],
            ["layer1_d", []],
            ["layer1_e", [
                ["layer2_c", [["layer3_a", []], ["layer3_b", []]]],
                ["layer2_d", [["layer3_c", [["layer4_a", []]]]]]
                ]
            ]
        ]

    meta = LayersParser()
    meta_layers = meta.layer_parser(EXAMPLE_3)
    assert meta_layers == output_data


def test_layer_parser_empty():
    meta = LayersParser()
    meta_layers = meta.layer_parser({})
    assert meta_layers == []


def test_layer_processing():
    input_data = [ 
            ["layer1_a", []],
            ["layer1_b", []],
            ["layer1_c",  [["layer2_a", []], ["layer2_b", []]]],
            ["layer1_d", []],
            ["layer1_e", [
                ["layer2_c", [["layer3_a", []], ["layer3_b", []]]],
                ["layer2_d", [["layer3_c", [["layer4_a", []]]]]]
                ]
            ],
            []
        ]
    
    output_data = [
    		["layer1_a", "layer1_b", "layer1_c", "layer1_d", "layer1_e"],
    		["layer2_a", "layer2_b", "layer2_c", "layer2_d"],
    		["layer3_a", "layer3_b", "layer3_c"],
    		["layer4_a"]
    		]
             
    meta = LayersParser()
    meta_layers = meta.layer_processing(input_data)
    assert meta_layers == output_data


def test_layer_processing_empty():
    meta = LayersParser()
    meta_layers = meta.layer_processing([])
    assert meta_layers == []


def test_layers_retrieval():
	input_data = [["layer_0"], ["layer_1"], ["layer_2"], ["layer_3"]] 
	output_data = {
			"layer_0": ["layer_0"],
			"layer_1": ["layer_1"],
			"layer_2": ["layer_2"],
			"layer_3": ["layer_3"]
			} 

	meta = LayersParser()
	meta_layers = meta.layers_retrieval(input_data)
	assert meta_layers == output_data

