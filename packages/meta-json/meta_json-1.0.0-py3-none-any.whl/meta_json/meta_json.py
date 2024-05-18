from typing import Dict, List, Union
from meta_json.attribute_parser import AttributesParser
from meta_json.layer_parser import LayersParser
from meta_json.type_parser import TypesParser


class MetaJson:
    """MetaJson main module."""

    def __init__(self, response: Union[Dict, List]):
        """Run all parsers in constructor."""
        self.response = response

    def attributes(self):
        """Return attributes result."""
        ap = AttributesParser()
        return ap.attribute_parser(self.response)

    def layers(self):
        """Return layers result."""
        lp = LayersParser()
        layers = lp.layer_processing(lp.layer_parser(self.response))
        return lp.layers_retrieval(layers)

    def types(self):
        """Return types result."""
        tp = TypesParser()
        return tp.type_parser(self.response)
