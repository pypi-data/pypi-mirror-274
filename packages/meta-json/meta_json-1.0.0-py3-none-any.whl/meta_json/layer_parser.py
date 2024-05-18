from typing import Dict, List, Any
from itertools import chain


class LayersParser:
    """Layer parser class."""

    def _soft_flatten(self, vals: List) -> List:
        """Turn double braces into one.

        Attributes
        ----------
        vals: list
            List with nested lists.

        Returns
        -------
        list
            List with reduced braces.
        """
        new_list = map(lambda x: x if isinstance(x, list) else [x], vals)
        return [*chain(*new_list)]

    def layer_parser(self, response: Any) -> List:
        """Given a JSON response, create a list showing attributes'
        depth per layer.

        Attributes
        ----------
        response:
            Deserialized JSON response, could be total or partial.

        Returns
        -------
        list
            List with key pairs [key, [subkeys]].
        """
        if isinstance(response, dict):
            return [[k, self.layer_parser(v)] for k, v in response.items()]
        elif isinstance(response, list):
            return self._soft_flatten([self.layer_parser(r) for r in response])
        else:
            return []

    def layer_processing(self, parsed_layer: List) -> List:
        """Create a list with sorted attribute layers from a previously parsed
        response into layers.

        Attributes
        ----------
        parsed_layer: list
            Result from layer_parser method.

        Returns
        -------
        list
            List with grouped attributes per layer [[layer1], [layer2]...].
        """
        layers = []
        while len(parsed_layer) > 0:
            layers.append([p.pop(0) for p in parsed_layer if len(p) > 0])
            bring_next = [p[0] for p in parsed_layer if len(p) > 0]
            parsed_layer = [*chain(*filter(lambda x: x != [], bring_next))]
        return layers

    @staticmethod
    def layers_retrieval(processed_layer: List) -> Dict:
        """Create a dictionary with the processed attribute layers.

        Attributes
        ----------
        processed_layer: list
            Result from layer_processing method.

        Returns
        -------
        dict
            Dictionary with attributes per layer {"layer_0": [attributes],...}.
        """
        return {f"layer_{idx}": val for idx, val in enumerate(processed_layer)}
