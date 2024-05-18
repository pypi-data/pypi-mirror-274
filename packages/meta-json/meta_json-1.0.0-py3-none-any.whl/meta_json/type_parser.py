import re
from typing import Dict, List, Any, Union


class TypesParser:
    """types parser class"""

    @staticmethod
    def _parse_datetimes(value: str) -> bool:
        """Determine if a string is a potential datetime.

        Attributes
        ----------
        value: str
            Variable to evaluate.

        Returns
        -------
        bool
            True if a datetime, false otherwise.
        """
        re_list = [
            r"(\d{4}(\-|\/)(0\d|1[0-2])(\-|\/)(0\d|1\d|2\d|3[0-1]))",
            r"((0\d|1\d|2\d|3[0-1])(\-|\/)(0\d|1[0-2])(\-|\/)\d{4})",
            r"((0\d|1[0-2])(\-|\/)(0\d|1\d|2\d|3[0-1])(\-|\/)\d{4})",
        ]
        rgx = re.compile("|".join(re_list))
        return bool(re.match(rgx, value))

    def type_parser(self, response: Any) -> Union[Union[Dict, List], str]:
        """Given a JSON response, create a dictionary with the value types
        instead of the actual values.

        Attributes
        ----------
        response:
            Deserialized JSON response, could be total or partial.

        Return
        -------
        list, dict, str
            Same response but with data types instead of values.
        """
        if isinstance(response, dict):
            return {k: self.type_parser(v) for k, v in response.items()}
        elif isinstance(response, list):
            return [self.type_parser(r) for r in response]
        else:
            if self._parse_datetimes(str(response)):
                return "datetime"
            return re.sub("(<class '|'>)", "", str(type(response)))
