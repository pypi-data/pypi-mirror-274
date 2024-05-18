from typing import List, Any
from itertools import chain


class AttributesParser:
    """Attribute parser class"""

    def _hard_flatten(self, vals: List) -> List:
        """Chain nested lists into a new one.

        Attributes
        ----------
        vals: list
            List with nested lists.

        Returns
        -------
        list
            List with all previous nested values.
        """
        # fmt: off
        flat_list = map(lambda x: self._hard_flatten(x) if isinstance(
            x, list) else [x], vals)
        return [*chain(*flat_list)]

    def attribute_parser(self, response: Any) -> List:
        """Given a JSON response, create a list grouping its attributes.

        Attributes
        ----------
        response:
            Deserialized JSON response, could be total or partial.

        Returns
        -------
        list
            List with grouped keys lists [primary keys, subkeys].
        """
        # fmt: off
        if isinstance(response, dict):
            return [list(response.keys()),
                    self.attribute_parser(list(response.values()))]
        elif isinstance(response, list):
            return self._hard_flatten(
                    [self.attribute_parser(r) for r in response])
        else:
            return []
